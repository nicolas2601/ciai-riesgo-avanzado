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


def _class_balance(catalog: pd.DataFrame) -> tuple[dict[str, int], dict[str, int], int, int]:
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
    municipalities = sorted(comparable.municipio.dropna().unique())
    months = pd.period_range(
        municipal_month.index.get_level_values("month").min(),
        municipal_month.index.get_level_values("month").max(),
        freq="M",
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
    annual_rows = [[str(year), system, str(int(count))] for (year, system), count in counts.items()]
    null_rows = [[column, str(int(count))] for column, count in catalog.isna().sum().items()]
    quantiles = [0, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99, 1]
    magnitude = new.mag.quantile(quantiles)
    depth = new.depth_km.quantile(quantiles)
    quantile_rows = [
        [f"{q:.0%}", _number(magnitude.loc[q]), _number(depth.loc[q])] for q in quantiles
    ]
    municipality_counts = new.municipio.value_counts()
    top_municipalities = [
        [name, str(int(value)), _number(value / len(new) * 100, 1)]
        for name, value in municipality_counts.head(10).items()
    ]
    los_santos_share = float(municipality_counts.get("LOS SANTOS", 0) / len(new) * 100)
    completeness = _maxc_by_year(catalog)
    month_classes, year_classes, month_rows, year_rows = _class_balance(catalog)
    class_rows = [
        [name, str(month_classes[name]), str(year_classes[name])] for name in CLASS_COLUMNS
    ]
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
        "Generado por `uv run --group reto python -m ml.eda.eda_sgc`; todas las cifras de este informe salen del script.",
        "",
        "## Cobertura y calidad",
        "",
        f"- Filas tras deduplicación: **{total:,}**; duplicados exactos removidos por `(datetime_utc, lat, lon, depth_km, mag)`: **{duplicates_removed}**.",
        f"- Rango: **{catalog.datetime_utc.min():%Y-%m-%d %H:%M UTC}–{catalog.datetime_utc.max():%Y-%m-%d %H:%M UTC}**. Sistemas: old **{int(catalog.source_system.eq('old').sum()):,}**, new **{int(catalog.source_system.eq('new').sum()):,}**.",
        "- Nulos por columna:",
        "",
        *_table(["Columna", "Nulos"], null_rows),
        "",
        "### Eventos por año y sistema",
        "",
        *_table(["Año", "Sistema", "Eventos"], annual_rows),
        "",
        "## Distribuciones (sistema nuevo; 2018-03 en adelante)",
        "",
        *_table(["Cuantil", "Magnitud", "Profundidad (km)"], quantile_rows),
        "",
        "### Municipios con más eventos",
        "",
        f"Los Santos representa **{_number(los_santos_share, 1)}%** de los {len(new):,} registros nuevos.",
        "",
        *_table(["Municipio", "Eventos", "% del catálogo nuevo"], top_municipalities),
        "",
        "## Completitud aproximada por año",
        "",
        "MAXC aproximado: magnitud con mayor frecuencia en histograma de ancho 0.1; se informa como descriptor de la moda, **no como Mc validada** ni como umbral de completitud robusto. Mezcla sistemas/escalas y cortes anuales; comparar con cautela.",
        "",
        *_table(["Año", "Sistema", "N", "Moda MAXC (M)"], completeness.values.tolist()),
        "",
        "**HIPÓTESIS:** el aumento de registros entre 2008 y 2012 es consistente con mejoras/cambios de instrumentación y cobertura; el catálogo por sí solo no establece causalidad.",
        "",
        "## Eventos de referencia del catálogo",
        "",
        "2015-03-10 usa la magnitud Mw disponible en el catálogo antiguo; puede diferir de estimaciones de otras agencias. Se muestran también los dos mayores eventos del sistema nuevo; no se convierten escalas.",
        "",
        *_table(["Fecha UTC", "M", "Tipo", "Prof. km", "Municipio", "Sistema"], reference_rows),
        "",
        "## Balance de clases por municipio",
        "",
        "Definición por período: bajo = sin M≥3; medio = al menos un M3.0–3.9 y sin M≥4; alto = al menos un M≥4. Sistema nuevo comparable desde 2018-03. Los conteos usan la cuadrícula completa de municipios observados × todos los meses y años del período; una celda sin evento catalogado queda como bajo.",
        "",
        f"Filas: municipio-mes **{month_rows:,}**; municipio-año **{year_rows:,}**.",
        "",
        *_table(["Clase", "Municipio-mes", "Municipio-año"], class_rows),
        "",
        f"**Recomendación:** usar municipio-mes para priorización temporal: hay {month_classes['alto']} períodos altos y {month_classes['medio']} medios ({month_rows:,} celdas; fuerte desbalance), lo que preserva resolución y permite horizonte mensual. Municipio-año reduce el número de celdas a {year_rows:,} y oculta variación intranual; usarlo como sensibilidad/agregado, no como unidad primaria. Reportar desbalance y comparar con baseline.",
        "",
        "## Limitaciones",
        "",
        "- El salto de versión old→new alrededor de 2018 impide interpretar diferencias de conteo/magnitud sin armonización; el tipo de magnitud se conserva.",
        "- MAXC anual con muestras y escalas mezcladas es solo exploratorio; no inferir cambio físico de amenaza desde más detecciones.",
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
