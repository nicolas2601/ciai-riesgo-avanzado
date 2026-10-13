"""Download the official SGC seismic catalog for Santander, one year per request.

Two systems answer different periods (verified 2026-10-13, HTTPS only):
  old: Consulta_Experta/consulsismo3.php             1993-06 .. 2018-02
  new: Consulta_Experta_Seiscomp/consulta_sismo.php  2018-03 .. today

Outputs data/raw/sgc/<system>_<year>.csv plus data/raw/sgc/provenance.json
(URL, filters, UTC download time, row count, sha256) so every number is traceable.

Usage: uv run --group reto python scripts/sgc_download.py [--from-year 2018] [--to-year 2026]
"""

import argparse
import csv
import hashlib
import html
import io
import json
import re
import time
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

import requests

BASE = "https://bdrsnc.sgc.gov.co/paginas1/catalogo"
OUT_DIR = Path("data/raw/sgc")
NEW_SYSTEM_FIRST_DAY = (2018, 3, 1)
OLD_SYSTEM_LAST_DAY = (2018, 2, 28)
TIMEOUT_S = 180
RETRIES = 3

SYSTEMS = {
    "old": {
        "url": f"{BASE}/Consulta_Experta/consulsismo3.php",
        "departamento": "SANTANDER",
        "mode_field": ("radiobutton", "cuadrante"),
        "extra": {"magnitudmwStart": "0", "magnitudmwEnd": "9"},
    },
    "new": {
        "url": f"{BASE}/Consulta_Experta_Seiscomp/consulta_sismo.php",
        "departamento": "27-Santander",
        "mode_field": ("ubi", "cuadrante"),
    },
}

DEFAULT_FILTERS = {
    "municipio": "",
    "longitudStart": "-90", "longitudEnd": "-66",
    "latitudStart": "-07", "latitudEnd": "15",
    "magnitudStart": "0", "magnitudEnd": "9",
    "depthStart": "0", "depthEnd": "700",
    "rmsStart": "0", "rmsEnd": "10",
    "gapStart": "0", "gapEnd": "360",
    "eprofmin": "0", "eprofmax": "999",
    "elongmin": "0", "elongmax": "999",
    "elatmin": "0", "elatmax": "999",
    "Submit": "Consultar",
}

ROW_START = re.compile(r"^\s*\d{4}-\d{2}-\d{2}")
TAG = re.compile(r"<[^>]+>")


def build_payload(system: str, first: str, last: str) -> dict:
    cfg = SYSTEMS[system]
    key, value = cfg["mode_field"]
    return {**DEFAULT_FILTERS, **cfg.get("extra", {}), "departamento": cfg["departamento"],
            "inicial": first, "final": last, key: value}


def fetch(system: str, first: str, last: str) -> str:
    payload = build_payload(system, first, last)
    for attempt in range(1, RETRIES + 1):
        try:
            resp = requests.post(SYSTEMS[system]["url"], data=payload, timeout=TIMEOUT_S)
            resp.raise_for_status()
            return resp.content.decode("utf-8", errors="replace")
        except requests.RequestException as exc:
            if attempt == RETRIES:
                raise RuntimeError(f"{system} {first}..{last} failed: {exc}") from exc
            time.sleep(2 * attempt)
    raise AssertionError("unreachable")


def parse_rows(page: str) -> list[list[str]]:
    if "mysql_fetch" in page:
        raise ValueError("SGC returned a MySQL error page (check form fields)")
    rows = []
    for chunk in re.split(r"<tr[^>]*>", page):
        cells = [html.unescape(TAG.sub("", c)).strip()
                 for c in re.findall(r"<td[^>]*>(.*?)(?=</td>|<td|$)", chunk, re.S)]
        if cells and ROW_START.match(cells[0]):
            rows.append(cells)
    return rows


EXCEL_LINK = re.compile(r"descargar_exel_experta\.php\?[^\"' >]+")
TOTAL_RECORDS = re.compile(r"tregistros=(\d+)")
XLSX_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"


def column_index(ref: str) -> int:
    letters = re.match(r"[A-Z]+", ref).group()
    index = 0
    for char in letters:
        index = index * 26 + ord(char) - 64
    return index - 1


def read_xlsx(content: bytes) -> list[list[str]]:
    """Minimal xlsx reader: openpyxl rejects the SGC stylesheet."""
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        shared = [
            "".join(t.text or "" for t in si.iter(f"{XLSX_NS}t"))
            for si in ET.fromstring(archive.read("xl/sharedStrings.xml")).iter(f"{XLSX_NS}si")
        ]
        sheet = ET.fromstring(archive.read("xl/worksheets/sheet1.xml"))
    rows = []
    for row in sheet.iter(f"{XLSX_NS}row"):
        cells: dict[int, str] = {}
        for cell in row.iter(f"{XLSX_NS}c"):
            value = cell.find(f"{XLSX_NS}v")
            if value is None or value.text is None:
                continue
            is_shared = cell.get("t") == "s"
            cells[column_index(cell.get("r"))] = shared[int(value.text)] if is_shared else value.text
        width = max(cells) + 1 if cells else 0
        rows.append([cells.get(i, "") for i in range(width)])
    return rows


def fetch_old_rows(first: str, last: str) -> list[list[str]]:
    """The old system pages the HTML at 35 rows; the Excel link returns every row."""
    page = fetch("old", first, last)
    link = EXCEL_LINK.search(page)
    if link is None and not parse_rows(page):
        return []
    if link is None:
        raise ValueError(f"old {first}..{last}: no Excel link in response")
    expected = int(TOTAL_RECORDS.search(link.group()).group(1))
    resp = requests.get(f"{BASE}/Consulta_Experta/{link.group()}", timeout=TIMEOUT_S)
    resp.raise_for_status()
    rows = read_xlsx(resp.content)[1:]
    if len(rows) != expected:
        raise ValueError(f"old {first}..{last}: expected {expected} rows, got {len(rows)}")
    return rows


def year_windows(system: str, from_year: int, to_year: int):
    today = datetime.now(timezone.utc).date()
    for year in range(from_year, to_year + 1):
        first, last = datetime(year, 1, 1).date(), datetime(year, 12, 31).date()
        if system == "old":
            last = min(last, datetime(*OLD_SYSTEM_LAST_DAY).date())
        else:
            first = max(first, datetime(*NEW_SYSTEM_FIRST_DAY).date())
            last = min(last, today)
        if first <= last:
            yield year, first.strftime("%d/%m/%Y"), last.strftime("%d/%m/%Y")


def write_year(system: str, year: int, first: str, last: str, rows: list[list[str]]) -> dict:
    path = OUT_DIR / f"{system}_{year}.csv"
    with path.open("w", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerows(rows)
    meta = {
        "system": system, "url": SYSTEMS[system]["url"], "year": year,
        "filters": build_payload(system, first, last), "rows": len(rows),
        "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "downloaded_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "file": str(path),
    }
    (OUT_DIR / f"{system}_{year}.meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    return meta


def download(system: str, from_year: int, to_year: int, skip_existing: bool) -> None:
    for year, first, last in year_windows(system, from_year, to_year):
        if skip_existing and (OUT_DIR / f"{system}_{year}.meta.json").exists():
            print(f"{system} {year}: skipped (already downloaded)")
            continue
        rows = fetch_old_rows(first, last) if system == "old" else parse_rows(fetch(system, first, last))
        meta = write_year(system, year, first, last, rows)
        print(f"{system} {year}: {meta['rows']} rows")


def merge_provenance() -> None:
    metas = [json.loads(p.read_text(encoding="utf-8")) for p in sorted(OUT_DIR.glob("*.meta.json"))]
    (OUT_DIR / "provenance.json").write_text(json.dumps(metas, indent=2), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--from-year", type=int, default=1993)
    parser.add_argument("--to-year", type=int, default=datetime.now(timezone.utc).year)
    parser.add_argument("--systems", nargs="+", default=["new", "old"], choices=list(SYSTEMS))
    parser.add_argument("--skip-existing", action="store_true", help="resume: keep years that already have a .meta.json")
    args = parser.parse_args()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for system in args.systems:
        download(system, args.from_year, args.to_year, args.skip_existing)
    merge_provenance()


if __name__ == "__main__":
    main()
