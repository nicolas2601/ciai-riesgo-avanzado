"""Generate reproducible exploratory statistics for the official SGC catalog."""

from __future__ import annotations

import argparse
import gzip
import tempfile
from pathlib import Path

import pandas as pd

from ml.eda.load_sgc import ROOT, load_catalog

DATA_DIR = ROOT / "data" / "sgc"
OUTPUT = ROOT / "docs" / "research" / "13-eda-sgc.md"
NEW_START = pd.Timestamp("2018-03-01", tz="UTC")
CLASS_COLUMNS = ["bajo", "medio", "alto"]


def load_gzip_catalog(data_dir: Path) -> tuple[pd.DataFrame, int]:
    """Expand versioned gzip exports temporarily, then reuse canonical loader."""
    with tempfile.TemporaryDirectory(prefix="sgc-eda-") as temporary:
        raw_dir = Path(temporary)
        for source in sorted(data_dir.glob("*.csv.gz")):
            target = raw_dir / source.name.removesuffix(".gz")
            with gzip.open(source, "rb") as compressed, target.open("wb") as output:
                output.write(compressed.read())
        frame = load_catalog(raw_dir)
    return frame, int(frame.attrs["duplicate_event_rows_removed"])


def _number(value: float, digits: int = 2) -> str:
    if pd.isna(value):
        return "—"
    return f"{value:.{digits}f}"


def _table(headers: list[str], rows: list[list[str]]) -> list[str]:
    lines = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    lines.extend("| " + " | ".join(row) + " |" for row in rows)
    return lines


def _classify(count_m3: int, count_m4: int) -> str:
    if count_m4:
        return "alto"
    if count_m3:
        return "medio"
    return "bajo"


def _class_balance(
    catalog: pd.DataFrame,
    municipalities: list[str] | None = None,
    months: pd.PeriodIndex | None = None,
    panel_path: Path | None = None,
) -> tuple[dict[str, int], dict[str, int], int, int]:
    comparable = catalog.loc[
        catalog.source_system.eq("new") & catalog.datetime_utc.ge(NEW_START)
    ].copy()
    comparable["month"] = comparable.datetime_utc.dt.tz_localize(None).dt.to_period("M")
    comparable["year"] = comparable.datetime_utc.dt.year
    comparable["m3"] = comparable.mag.ge(3)
    comparable["m4"] = comparable.mag.ge(4)
    municipal_month = comparable.groupby(["municipio", "month"], observed=True).agg(
        m3=("m3", "sum"), m4=("m4", "sum")
    )
    if panel_path is not None and panel_path.exists():
        panel = pd.read_csv(
            panel_path,
            usecols=["divipola", "month", "coverage_complete", "n_m_ge_3_mes", "n_m_ge_4_mes"],
        )
        panel = panel.loc[panel.coverage_complete].copy()
        panel["year"] = panel.month.str[:4].astype(int)
        panel["class"] = [
            _classify(int(m3), int(m4))
            for m3, m4 in zip(panel.n_m_ge_3_mes, panel.n_m_ge_4_mes, strict=True)
        ]
        month_classes = panel["class"].value_counts().reindex(CLASS_COLUMNS, fill_value=0)
        annual = panel.groupby(["divipola", "year"], observed=True).agg(
            m3=("n_m_ge_3_mes", "sum"), m4=("n_m_ge_4_mes", "sum")
        )
        year_classes = (
            annual.apply(lambda row: _classify(int(row.m3), int(row.m4)), axis=1)
            .value_counts()
            .reindex(CLASS_COLUMNS, fill_value=0)
        )
        return (
            {key: int(month_classes[key]) for key in CLASS_COLUMNS},
            {key: int(year_classes[key]) for key in CLASS_COLUMNS},
            len(panel),
            len(annual),
        )

    municipalities = municipalities or sorted(comparable.municipio.dropna().unique())
    months = (
        months
        if months is not None
        else pd.period_range(
            municipal_month.index.get_level_values("month").min(),
            municipal_month.index.get_level_values("month").max(),
            freq="M",
        )
    )
    full_month_index = pd.MultiIndex.from_product(
        [municipalities, months], names=["municipio", "month"]
    )
    municipal_month = municipal_month.reindex(full_month_index, fill_value=0)
    month_classes = (
        municipal_month.apply(lambda row: _classify(int(row.m3), int(row.m4)), axis=1)
        .value_counts()
        .reindex(CLASS_COLUMNS, fill_value=0)
        .to_dict()
    )
    municipal_year = comparable.groupby(["municipio", "year"], observed=True).agg(
        m3=("m3", "sum"), m4=("m4", "sum")
    )
    years = range(int(comparable.year.min()), int(comparable.year.max()) + 1)
    full_year_index = pd.MultiIndex.from_product(
        [municipalities, years], names=["municipio", "year"]
    )
    municipal_year = municipal_year.reindex(full_year_index, fill_value=0)
    year_classes = (
        municipal_year.apply(lambda row: _classify(int(row.m3), int(row.m4)), axis=1)
        .value_counts()
        .reindex(CLASS_COLUMNS, fill_value=0)
        .to_dict()
    )
    return (
        {key: int(month_classes[key]) for key in CLASS_COLUMNS},
        {key: int(year_classes[key]) for key in CLASS_COLUMNS},
        len(municipal_month),
        len(municipal_year),
    )


def _maxc_by_year(catalog: pd.DataFrame) -> pd.DataFrame:
    rows = []
    new_years = catalog.loc[catalog.source_system.eq("new"), "datetime_utc"].dt.year.unique()
    for year in sorted(catalog.datetime_utc.dt.year.unique()):
        source = "new" if year in new_years else "old"
        values = catalog.loc[
            catalog.source_system.eq(source) & catalog.datetime_utc.dt.year.eq(year), "mag"
        ].dropna()
        if values.empty:
            rows.append([str(year), source, "0", "—"])
            continue
        bins = values.mul(10).round().astype(int).value_counts()
        mode = int(bins.idxmax()) / 10
        rows.append([str(year), source, str(len(values)), _number(mode, 1)])
    return pd.DataFrame(rows, columns=["year", "system", "events", "mc"])


def build_report(catalog: pd.DataFrame, duplicates_removed: int) -> str:
    total = len(catalog)
    new = catalog.loc[catalog.source_system.eq("new")].copy()
    counts = catalog.groupby([catalog.datetime_utc.dt.year, "source_system"]).size()
    annual_rows = [
        [str(year), str(int(counts.get((year, system), 0)))]
        for year in sorted(catalog.datetime_utc.dt.year.unique())
        for system in ("old", "new")
        if counts.get((year, system), 0)
    ]
    null_rows = [[column, str(int(count))] for column, count in catalog.isna().sum().items()]
    quantiles = [0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1]
    magnitude = new.mag.quantile(quantiles)
    depth = new.depth_km.quantile(quantiles)
    quantile_rows = [
        [f"{q:.0%}", _number(magnitude.loc[q]), _number(depth.loc[q])] for q in quantiles
    ]
    municipality_counts = new.municipio.value_counts()
    top_municipalities = [
        [name, f"{int(value):,}", _number(value / len(new) * 100, 1)]
        for name, value in municipality_counts.head(10).items()
    ]
    los_santos_share = float(municipality_counts.get("LOS SANTOS", 0) / len(new) * 100)
    completeness = _maxc_by_year(catalog)
    panel_path = ROOT / "data" / "panel" / "panel_municipio_mes.csv.gz"
    month_classes, year_classes, month_row_count, year_row_count = _class_balance(
        catalog, panel_path=panel_path
    )
    class_rows = [
        [name, str(month_classes[name]), str(year_classes[name])] for name in CLASS_COLUMNS
    ]
    annual_compact = []
    for row in annual_rows:
        year, count = row
        existing = next((item for item in annual_compact if item[0] == year), None)
        if existing is None:
            annual_compact.append([year, "0", "0"])
            existing = annual_compact[-1]
        source = "old" if counts.get((int(year), "old"), 0) else "new"
        existing[1 if source == "old" else 2] = f"{int(count):,}"
    maxc_summary = ", ".join(
        f"{row.year} {row.system[0]}:{row.mc}" for row in completeness.itertuples()
    )
    high_events = (
        new.loc[new.datetime_utc.ge(NEW_START) & new.mag.ge(5)]
        .sort_values(["mag", "datetime_utc"], ascending=[False, True])
        .drop_duplicates(subset=["datetime_utc", "lat", "lon", "depth_km", "mag"])
        .head(2)
    )
    reference_2023 = new.loc[new.datetime_utc.dt.strftime("%Y-%m-%d").eq("2023-03-10")].nlargest(
        1, "mag"
    )
    high_rows = [
        [
            row.datetime_utc.strftime("%Y-%m-%d %H:%M UTC"),
            _number(row.mag, 1),
            str(row.mag_type),
            _number(row.depth_km, 1),
            str(row.municipio),
            str(row.source_system),
        ]
        for row in high_events.itertuples()
    ]
    reference_2015 = catalog.loc[
        catalog.datetime_utc.dt.strftime("%Y-%m-%d").eq("2015-03-10")
    ].nlargest(1, "mag")
    reference_rows = []
    if not reference_2015.empty:
        row = reference_2015.iloc[0]
        reference_rows.append(
            [
                row.datetime_utc.strftime("%Y-%m-%d %H:%M UTC"),
                _number(row.mag, 1),
                str(row.mag_type),
                _number(row.depth_km, 1),
                str(row.municipio),
                str(row.source_system),
            ]
        )
    reference_rows.extend(
        [
            row.datetime_utc.strftime("%Y-%m-%d %H:%M UTC"),
            _number(row.mag, 1),
            str(row.mag_type),
            _number(row.depth_km, 1),
            str(row.municipio),
            str(row.source_system),
        ]
        for row in reference_2023.itertuples()
    )
    reference_rows.extend(high_rows)
    lines = [
        "# EDA del catálogo sísmico SGC",
        "",
        "Generado por `uv run --group reto python -m ml.eda.eda_sgc`; cifras generadas por script.",
        "",
        "## Cobertura y calidad",
        "",
        f"- Filas tras deduplicación: **{total:,}**; duplicados exactos removidos por `(datetime_utc, lat, lon, depth_km, mag)`: **{duplicates_removed}**.",
        f"- Rango: **{catalog.datetime_utc.min():%Y-%m-%d %H:%M UTC}–{catalog.datetime_utc.max():%Y-%m-%d %H:%M UTC}**. Sistemas: old **{int(catalog.source_system.eq('old').sum()):,}**, new **{int(catalog.source_system.eq('new').sum()):,}**.",
        "- Nulos: " + "; ".join(f"{name}={count}" for name, count in null_rows) + ".",
        "### Eventos por año y sistema",
        "",
        "| Año | Old | New |",
        "|---|---:|---:|",
        *[
            f"| {year} | {old_count} | {new_count} |"
            for year, old_count, new_count in annual_compact
        ],
        "",
        "## Distribuciones (new; 2018-03+)",
        "",
        "Cuantil: "
        + "; ".join(f"{q} M={mag}, z={depth} km" for q, mag, depth in quantile_rows)
        + ".",
        "### Municipios con más eventos",
        "",
        f"Los Santos: **{_number(los_santos_share, 1)}%** de {len(new):,} eventos new.",
        "",
        "; ".join(f"{name}: {count} ({pct}%)" for name, count, pct in top_municipalities) + ".",
        "",
        "## Completitud aproximada por año",
        "",
        "MAXC = moda anual de bins 0.1; aproximación exploratoria, no Mc validada. Escalas old/new difieren.",
        "",
        "Año/sistema:Mc/N — " + maxc_summary + ".",
        "",
        "**HIPÓTESIS:** el aumento de registros entre 2008 y 2012 es consistente con mejoras/cambios de instrumentación y cobertura; el catálogo por sí solo no establece causalidad.",
        "",
        "## Eventos de referencia del catálogo",
        "",
        "2015-03-10 Mw old y dos mayores new; escalas no convertidas.",
        "",
        *_table(["Fecha UTC", "M", "Tipo", "Prof. km", "Municipio", "Sistema"], reference_rows),
        "",
        "## Balance de clases por municipio",
        "",
        "Clases: bajo sin M≥3; medio ≥1 M3.0–3.9 y sin M≥4; alto ≥1 M≥4. New comparable desde 2018-03. Municipio-mes usa cuadrícula del panel (87×103); municipio-año 2018–2026. Vacíos = bajo.",
        "",
        f"Filas: municipio-mes **{month_row_count:,}**; municipio-año **{year_row_count:,}**.",
        "",
        *_table(["Clase", "Municipio-mes", "Municipio-año"], class_rows),
        "",
        f"**Recomendación:** municipio-mes preserva horizonte mensual ({month_classes['alto']} alto, {month_classes['medio']} medio de {month_row_count:,}; desbalance). Municipio-año agrega a {year_row_count:,} celdas y pierde variación intranual; usar como sensibilidad, comparar baseline.",
        "",
        "## Limitaciones",
        "",
        "- old/new y escalas no armonizadas; MAXC exploratoria. Más detecciones no prueba cambio físico de amenaza.",
        "",
    ]
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", type=Path, default=DATA_DIR)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    catalog, duplicates_removed = load_gzip_catalog(args.data_dir)
    report = build_report(catalog, duplicates_removed)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(f"Wrote {args.output} ({len(report.splitlines())} lines)")


if __name__ == "__main__":
    main()
