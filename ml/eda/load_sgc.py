"""Load both SGC export schemas without equating different magnitude scales."""

import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
NEW_COLUMNS = [
    "datetime",
    "lat",
    "lon",
    "depth_km",
    "mag",
    "mag_type",
    "phases",
    "rms",
    "gap",
    "err_lat",
    "err_lon",
    "err_depth",
    "region",
    "link1",
    "link2",
    "link3",
    "status",
]
OLD_COLUMNS = [
    "date",
    "time",
    "lat",
    "lon",
    "depth_km",
    "ml",
    "mw",
    "department",
    "municipio",
    "phases",
    "rms",
    "gap",
    "err_lat",
    "err_lon",
    "err_depth",
    "status",
]
COMMON_COLUMNS = [
    "datetime_utc",
    "lat",
    "lon",
    "depth_km",
    "mag",
    "mag_type",
    "municipio",
    "source_system",
    "rms",
    "gap",
    "phases",
    "source_file",
]


def normalize_municipality(value: str) -> str:
    name = str(value).split(" - ")[0].split(",")[0]
    name = unicodedata.normalize("NFKD", name)
    name = "".join(char for char in name if not unicodedata.combining(char))
    return " ".join(name.replace("_", " ").replace("-", " ").upper().split())


def _read_file(path: Path) -> pd.DataFrame:
    system = path.name.split("_")[0]
    columns = NEW_COLUMNS if system == "new" else OLD_COLUMNS
    try:
        frame = pd.read_csv(path, header=None, dtype=str, keep_default_na=False)
    except pd.errors.EmptyDataError:
        return pd.DataFrame(columns=COMMON_COLUMNS)
    if frame.shape[1] != len(columns):
        raise ValueError(f"{path}: expected {len(columns)} columns, got {frame.shape[1]}")
    frame.columns = columns
    if system == "old":
        frame["datetime"] = frame["date"] + " " + frame["time"]
        mw = pd.to_numeric(frame.mw, errors="coerce")
        frame["mag"] = mw.fillna(pd.to_numeric(frame.ml, errors="coerce"))
        frame["mag_type"] = mw.notna().map({True: "Mw", False: "Ml"})
    else:
        frame["municipio"] = frame.region.map(normalize_municipality)
    frame["datetime_utc"] = pd.to_datetime(
        frame.datetime, format="mixed", utc=True, errors="coerce"
    )
    if frame.datetime_utc.isna().any():
        raise ValueError(f"{path}: invalid event date in {frame.datetime_utc.isna().sum()} rows")
    for column in ["lat", "lon", "depth_km", "mag", "rms", "gap", "phases"]:
        frame[column] = pd.to_numeric(frame[column], errors="coerce")
    frame["municipio"] = frame.municipio.map(normalize_municipality)
    frame["source_system"] = system
    frame["source_file"] = path.name
    return frame[COMMON_COLUMNS]


def load_catalog(raw_dir: str | Path = ROOT / "data/raw/sgc") -> pd.DataFrame:
    """Read available old/new CSVs; invalid timestamps fail rather than disappear."""
    files = sorted(Path(raw_dir).glob("old_*.csv")) + sorted(Path(raw_dir).glob("new_*.csv"))
    if not files:
        raise FileNotFoundError(f"No SGC CSV exports in {raw_dir}")
    frames = [_read_file(path) for path in files]
    catalog = pd.concat(frames, ignore_index=True)
    before = len(catalog)
    keys = ["datetime_utc", "lat", "lon", "depth_km", "mag"]
    catalog = (
        catalog.drop_duplicates(subset=keys).sort_values("datetime_utc").reset_index(drop=True)
    )
    catalog.attrs["duplicate_event_rows_removed"] = before - len(catalog)
    return catalog
