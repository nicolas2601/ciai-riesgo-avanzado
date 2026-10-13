"""Build a coverage-aware municipal panel and generated data dictionary."""

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from ml.eda.load_sgc import ROOT, load_catalog, normalize_municipality
from ml.eda.panel_features import (
    COUNT_COLUMNS,
    FEATURE_COLUMNS,
    add_detection_context,
    add_history,
    add_neighbors,
    aggregate_events,
)

# Exact alias confirmed by the SGC Santander municipality list; never fuzzy matching.
SANTANDER_ALIASES = {"EL CARMEN": "EL CARMEN DE CHUCURI"}


def audit_aliases(catalog: pd.DataFrame) -> pd.DataFrame:
    catalog = catalog.copy()
    if "municipio_sgc" not in catalog:
        catalog["municipio_sgc"] = catalog.municipio
    catalog["municipio"] = catalog.municipio.replace(SANTANDER_ALIASES)
    return catalog


def build_panel(catalog, municipalities, covered_months, population=None):
    municipalities = municipalities.copy().sort_values("zone_id").reset_index(drop=True)
    municipalities["municipio"] = municipalities.municipality.map(normalize_municipality)
    covered = pd.PeriodIndex(covered_months, freq="M")
    if covered.empty:
        raise ValueError("No complete covered months")
    months = pd.period_range(covered.min(), covered.max(), freq="M")
    grid = pd.MultiIndex.from_product([municipalities.zone_id, months], names=["zone_id", "month"])
    panel = grid.to_frame(index=False).merge(municipalities, on="zone_id", validate="many_to_one")
    events = audit_aliases(catalog[catalog.source_system == "new"])
    aggregated = aggregate_events(events)
    panel = panel.merge(aggregated, on=["municipio", "month"], how="left", validate="one_to_one")
    panel["coverage_complete"] = panel.month.isin(covered)
    for column in COUNT_COLUMNS:
        panel[column] = panel[column].fillna(0).where(panel.coverage_complete)
    statistic_columns = [
        c
        for c in aggregated.columns
        if c not in ["municipio", "month", *COUNT_COLUMNS, "last_event", "last_m3"]
    ]
    empty = panel.n_eventos_mes.eq(0) & panel.coverage_complete
    panel.loc[empty, statistic_columns] = 0.0
    panel = add_history(panel)
    panel = add_neighbors(panel, municipalities)
    panel = add_detection_context(panel, events)
    panel = add_targets(panel)
    panel = join_population(panel, population)
    return finish_panel(panel)


def join_population(panel: pd.DataFrame, population: pd.DataFrame | None) -> pd.DataFrame:
    panel = panel.copy()
    panel["poblacion"] = np.nan
    if population is None:
        return panel
    population = population[["divipola", "anio", "poblacion"]].copy()
    population["divipola"] = population.divipola.astype(str).str.zfill(5)
    population["anio"] = pd.to_numeric(population.anio, errors="raise").astype(int)
    population["poblacion"] = pd.to_numeric(population.poblacion, errors="raise")
    panel["divipola"] = panel.zone_id.astype(str).str.zfill(5)
    panel["anio"] = panel.month.dt.year
    panel = panel.drop(columns="poblacion").merge(
        population, on=["divipola", "anio"], how="left", validate="many_to_one"
    )
    return panel.drop(columns="anio")


def finish_panel(panel: pd.DataFrame) -> pd.DataFrame:
    panel["centroid_lat"], panel["centroid_lon"] = panel.lat, panel.lon
    panel["divipola"] = panel.zone_id
    panel["source_system"] = "new"
    panel["history_12m_complete"] = panel.n_eventos_12m.notna()
    panel["eligible"] = panel.history_12m_complete & panel.coverage_complete
    panel["feature_cutoff"] = (panel.month.dt.to_timestamp() + pd.offsets.MonthEnd(1)).dt.strftime(
        "%Y-%m-%d"
    )
    panel = panel.loc[panel.coverage_complete].copy()
    panel["month"] = panel.month.astype(str)
    keep = [
        "zone_id",
        "divipola",
        "municipio",
        "month",
        "feature_cutoff",
        "source_system",
        "coverage_complete",
        "history_12m_complete",
        "eligible",
        *FEATURE_COLUMNS,
    ]
    keep += [c for c in panel.columns if c.startswith("target_")]
    return panel[keep].reset_index(drop=True)


def feature_detail(name: str) -> str:
    if name == "poblacion":
        return "personas; DANE CNPV2018 proyección/estimación del año del corte, retrospectiva"
    if name.startswith("n_"):
        return "eventos registrados; ventana indicada; SGC (vecinos radio50km, excluye propio)"
    if name.startswith("frac_"):
        return "proporción; mes; SGC; bandas[0,30),[30,70),[70,300],(300,+inf)"
    if "prof_" in name:
        return "km; mes; SGC"
    if name.startswith("dias_"):
        return "días desde último registrado hasta fin de mes; -1=censurado; SGC"
    if name.startswith("centroid_"):
        return "grados; snapshot directorio DIVIPOLA oficial en repo"
    if name.startswith("mc_"):
        return "magnitud; MAXC histograma0.1, SOLO12meses anteriores/incluidoactual; SGC"
    if name == "year_context":
        return "año calendario del corte; contexto, NO medición de estaciones"
    return "magnitud/RMS segundos/gap grados/fases; SGC; ventana indicada"


def add_targets(panel):
    groups = panel.groupby("zone_id", sort=False)
    covered_next = groups.coverage_complete.shift(-1).fillna(False).astype(bool)
    magnitude_next = groups.mag_max_mes.shift(-1)
    panel["target_n_eventos_mes_siguiente"] = groups.n_eventos_mes.shift(-1).where(covered_next)
    levels = np.select(
        [magnitude_next.ge(4), magnitude_next.ge(3)], ["alto", "medio"], default="bajo"
    )
    panel["target_clase_mes_siguiente"] = pd.Series(levels, index=panel.index).where(
        covered_next & magnitude_next.notna()
    )
    panel["target_actividad_m3_mes_siguiente"] = (
        magnitude_next.ge(3).astype(float).where(covered_next & magnitude_next.notna())
    )
    panel["target_month"] = (panel.month + 1).astype(str)
    return panel


def covered_months(raw_dir, system="new"):
    covered = set()
    for path in Path(raw_dir).glob(f"{system}_*.meta.json"):
        record = json.loads(path.read_text())
        first = pd.to_datetime(record["filters"]["inicial"], format="%d/%m/%Y")
        last = pd.to_datetime(record["filters"]["final"], format="%d/%m/%Y")
        first = max(
            first, pd.Timestamp("2018-03-01") if system == "new" else pd.Timestamp("1993-06-01")
        )
        last = min(
            last, pd.Timestamp.now(tz="UTC").tz_localize(None).normalize() - pd.Timedelta(days=1)
        )
        for month in pd.period_range(first, last, freq="M"):
            if month.start_time >= first and month.end_time.normalize() <= last:
                covered.add(month)
    return pd.PeriodIndex(sorted(covered), freq="M")


def write_dictionary(panel, catalog, path, unmatched):
    lines = [
        "# Diccionario del panel SGC",
        "",
        "Generado por `python -m ml.eda.build_panel`; no editar cifras a mano.",
        f"HECHO: {len(panel):,} filas, {len(panel.columns)} columnas, {len(FEATURE_COLUMNS)} features SGC/DIVIPOLA/DANE; catálogo unificado {len(catalog):,} eventos.",
        f"HECHO: municipios sin cruce: {unmatched}.",
        "",
        "| Feature | Tipo | Unidad / ventana / fuente | Justificación |",
        "|---|---|---|---|",
    ]
    for name in FEATURE_COLUMNS:
        lines.append(
            f"| {name} | {panel[name].dtype} | {feature_detail(name)} | Actividad/recencia/profundidad/calidad/contexto; solo pasado |"
        )
    lines += [
        "",
        "`energia_log_3m`=ln(1+sum(10^(1.5*M))) de3meses: índice relativo de magnitudes reportadas, NO joules ni homogeneización Mw.",
        "Estadísticas de meses cubiertos sin eventos usan0 como sentinel junto a hay_eventos_mes; historia incompleta y estadísticas indefinidas quedan nulas.",
        "Panel principal usa solo sistema nuevo desde2018-03. Catálogo antiguo incluido en archivo unificado, NO en conteos del panel comparable.",
        "Targets separados: siguiente mes calendario completo; alto siM>=4, medio siM>=3sinM>=4, bajo sinM>=3. Último/gap sin seguimiento: target nulo.",
        "Imputación/escalado corresponden a entrenamiento, nunca rellenar con futuro. Población DANE es proyección/estimación retrospectiva CNPV2018, NO observación ni disponibilidad histórica as-of demostrada.",
        "Alias exacto auditado dentro de Santander y confirmado por crosswalk DANE: EL CARMEN→EL CARMEN DE CHUCURI, DIVIPOLA68235; municipio_sgc conserva nombre previo.",
        f"Cruce DANE: {panel.loc[panel.poblacion.notna(), 'divipola'].nunique()}/{panel.divipola.nunique()} municipios; {panel.poblacion.isna().sum()} filas sin población. area_total_o_cabecera NO es km²: no se inventa densidad.",
        "Más detecciones no prueba más sismicidad. Mc MAXC es aproximación regional, puede subestimar completitud; conteos M3/M4 fijos y contexto mensual/año permiten sensibilidad, no garantizan corrección de instrumentación.",
        "Reward recomendado: target_actividad_m3_mes_siguiente, NO conteo crudo sin declarar sesgo; escoger umbral fijo Mc SOLO con train. Mc por año completo es EDA, no feature as-of.",
        "",
        "## Balance real de target mensual",
        "| Clase | Filas |",
        "|---|---|",
    ]
    lines += [
        f"| {key} | {value} |"
        for key, value in panel.target_clase_mes_siguiente.value_counts(dropna=False).items()
    ]
    lines += ["", "## Tres filas reales", "```text", panel.head(3).to_string(index=False), "```"]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--raw-dir", type=Path, default=ROOT / "data/raw/sgc")
    args = parser.parse_args()
    catalog = load_catalog(args.raw_dir)
    completed = {p.name.replace(".meta.json", ".csv") for p in args.raw_dir.glob("*.meta.json")}
    catalog = audit_aliases(catalog[catalog.source_file.isin(completed)])
    municipalities = pd.DataFrame(
        json.loads((ROOT / "app/api/data/municipios_santander.json").read_text())
    )
    known = set(municipalities.municipality.map(normalize_municipality))
    unmatched = catalog.loc[~catalog.municipio.isin(known), "municipio"].value_counts().to_dict()
    population_path = ROOT / "data/external_pub/dane_poblacion_municipal.csv"
    population = (
        pd.read_csv(population_path, dtype={"divipola": str}) if population_path.exists() else None
    )
    panel = build_panel(catalog, municipalities, covered_months(args.raw_dir), population)
    save_outputs(panel, catalog, unmatched, args.raw_dir)


def save_outputs(panel, catalog, unmatched, raw_dir):
    output = ROOT / "data/panel"
    output.mkdir(parents=True, exist_ok=True)
    catalog.to_csv(
        output / "catalogo_unificado.csv.gz",
        index=False,
        compression={"method": "gzip", "mtime": 0},
    )
    panel.to_csv(
        output / "panel_municipio_mes.csv.gz",
        index=False,
        compression={"method": "gzip", "mtime": 0},
    )
    summary = {
        "rows": len(panel),
        "columns": len(panel.columns),
        "features": FEATURE_COLUMNS,
        "download_finished": (raw_dir / "provenance.json").exists(),
        "unmatched": unmatched,
        "duplicates_removed": catalog.attrs.get("duplicate_event_rows_removed", 0),
        "nulls": panel.isna().sum().to_dict(),
        "target_balance": panel.target_clase_mes_siguiente.value_counts().to_dict(),
    }
    (output / "metadata.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    write_dictionary(panel, catalog, ROOT / "docs/data/diccionario.md", unmatched)
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    print(panel.head(3).to_string(index=False))


if __name__ == "__main__":
    main()
