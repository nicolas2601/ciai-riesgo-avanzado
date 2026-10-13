"""Past-only monthly features; undefined history remains missing, never future-filled."""

import numpy as np
import pandas as pd

FEATURE_COLUMNS = [
    "n_eventos_mes",
    "n_eventos_3m",
    "n_eventos_12m",
    "mag_max_mes",
    "mag_max_3m",
    "mag_media_mes",
    "mag_std_mes",
    "n_m_ge_3_mes",
    "n_m_ge_3_12m",
    "n_m_ge_4_mes",
    "n_m_ge_4_12m",
    "energia_log_3m",
    "prof_media_mes",
    "prof_std_mes",
    "frac_prof_lt30",
    "frac_30_70",
    "frac_70_300",
    "frac_gt300",
    "rms_media_mes",
    "gap_media_mes",
    "fases_media_mes",
    "dias_desde_ultimo_evento",
    "dias_desde_ultimo_m3",
    "n_eventos_vecinos_mes",
    "centroid_lat",
    "centroid_lon",
    "hay_eventos_mes",
    "mc_maxc_12m",
    "n_m_ge_mc_mes",
    "n_eventos_departamento_mes",
    "year_context",
    "poblacion",
]
COUNT_COLUMNS = ["n_eventos_mes", "n_m_ge_3_mes", "n_m_ge_4_mes", "energy_sum"]
EARTH_RADIUS_KM = 6371.0088
NEIGHBOR_RADIUS_KM = 50.0


def aggregate_events(events: pd.DataFrame) -> pd.DataFrame:
    events = events.copy()
    events["month"] = events.datetime_utc.dt.tz_localize(None).dt.to_period("M")
    events["m3"] = events.mag.ge(3).astype(int)
    events["m4"] = events.mag.ge(4).astype(int)
    events["energy"] = np.power(10.0, 1.5 * events.mag)
    events["last_m3"] = events.datetime_utc.where(events.mag.ge(3))
    for name, condition in {
        "frac_prof_lt30": events.depth_km.lt(30),
        "frac_30_70": events.depth_km.ge(30) & events.depth_km.lt(70),
        "frac_70_300": events.depth_km.ge(70) & events.depth_km.le(300),
        "frac_gt300": events.depth_km.gt(300),
    }.items():
        events[name] = condition.astype(float).where(events.depth_km.notna())
    specification = {
        "n_eventos_mes": ("datetime_utc", "size"),
        "mag_max_mes": ("mag", "max"),
        "mag_media_mes": ("mag", "mean"),
        "mag_std_mes": ("mag", "std"),
        "n_m_ge_3_mes": ("m3", "sum"),
        "n_m_ge_4_mes": ("m4", "sum"),
        "energy_sum": ("energy", "sum"),
        "prof_media_mes": ("depth_km", "mean"),
        "prof_std_mes": ("depth_km", "std"),
        "rms_media_mes": ("rms", "mean"),
        "gap_media_mes": ("gap", "mean"),
        "fases_media_mes": ("phases", "mean"),
        "last_event": ("datetime_utc", "max"),
        "last_m3": ("last_m3", "max"),
    }
    specification.update(
        {
            name: (name, "mean")
            for name in ["frac_prof_lt30", "frac_30_70", "frac_70_300", "frac_gt300"]
        }
    )
    return events.groupby(["municipio", "month"]).agg(**specification).reset_index()


def add_history(panel: pd.DataFrame) -> pd.DataFrame:
    groups = panel.groupby("zone_id", sort=False)
    for column, window, output, operation in [
        ("n_eventos_mes", 3, "n_eventos_3m", "sum"),
        ("n_eventos_mes", 12, "n_eventos_12m", "sum"),
        ("mag_max_mes", 3, "mag_max_3m", "max"),
        ("n_m_ge_3_mes", 12, "n_m_ge_3_12m", "sum"),
        ("n_m_ge_4_mes", 12, "n_m_ge_4_12m", "sum"),
        ("energy_sum", 3, "energia_log_3m", "sum"),
    ]:
        panel[output] = groups[column].transform(
            lambda values, window=window, operation=operation: getattr(
                values.rolling(window, min_periods=window), operation
            )()
        )
    panel["energia_log_3m"] = np.log1p(panel.energia_log_3m)
    cutoff = pd.to_datetime(panel.month.astype(str), utc=True) + pd.offsets.MonthBegin(1)
    cutoff -= pd.Timedelta(nanoseconds=1)
    for column, output in [
        ("last_event", "dias_desde_ultimo_evento"),
        ("last_m3", "dias_desde_ultimo_m3"),
    ]:
        last = groups[column].ffill()
        panel[output] = (cutoff - last).dt.days.fillna(-1)
    panel["hay_eventos_mes"] = panel.n_eventos_mes.gt(0).astype(int)
    return panel


def add_neighbors(panel: pd.DataFrame, municipalities: pd.DataFrame) -> pd.DataFrame:
    coordinates = np.radians(municipalities[["lat", "lon"]].to_numpy(float))
    delta = coordinates[:, None, :] - coordinates[None, :, :]
    haversine = np.sin(delta[:, :, 0] / 2) ** 2
    haversine += (
        np.cos(coordinates[:, 0])[:, None]
        * np.cos(coordinates[:, 0])[None, :]
        * np.sin(delta[:, :, 1] / 2) ** 2
    )
    distance = 2 * EARTH_RADIUS_KM * np.arcsin(np.sqrt(np.clip(haversine, 0, 1)))
    neighbors = distance <= NEIGHBOR_RADIUS_KM
    np.fill_diagonal(neighbors, False)
    counts = panel.pivot(index="month", columns="zone_id", values="n_eventos_mes")
    counts = counts.reindex(columns=municipalities.zone_id)
    values = pd.DataFrame(counts.to_numpy() @ neighbors, index=counts.index, columns=counts.columns)
    values = values.rename_axis(columns="zone_id").stack().rename("n_eventos_vecinos_mes")
    return panel.join(values, on=["month", "zone_id"])


def add_detection_context(panel: pd.DataFrame, events: pd.DataFrame) -> pd.DataFrame:
    panel["mc_maxc_12m"] = np.nan
    panel["n_m_ge_mc_mes"] = np.nan
    panel["n_eventos_departamento_mes"] = panel.groupby("month").n_eventos_mes.transform("sum")
    panel["year_context"] = panel.month.dt.year
    for month in panel.month.unique():
        start = month.start_time.tz_localize("UTC")
        end = (month + 1).start_time.tz_localize("UTC")
        history_start = (month - 11).start_time.tz_localize("UTC")
        history = events.loc[events.datetime_utc.ge(history_start) & events.datetime_utc.lt(end)]
        bins = history.mag.dropna().mul(10).round().astype(int).value_counts().sort_index()
        if bins.empty:
            continue
        mc = bins.idxmax() / 10
        current = events.loc[
            events.datetime_utc.ge(start) & events.datetime_utc.lt(end) & events.mag.ge(mc)
        ]
        counts = current.groupby("municipio").size()
        mask = panel.month.eq(month)
        panel.loc[mask, "mc_maxc_12m"] = mc
        panel.loc[mask, "n_m_ge_mc_mes"] = panel.loc[mask, "municipio"].map(counts).fillna(0)
    return panel
