import csv

import pandas as pd
import pytest

from ml.eda.load_sgc import load_catalog

ROWS = {
    "new_2018.csv": [
        "2018-03-01 00:49:05",
        6.8,
        -73.1,
        150,
        2.5,
        "MLr",
        10,
        0.3,
        80,
        1,
        1,
        2,
        "Los Sántos - Santander, Colombia",
        "",
        "",
        "",
        "manual",
    ],
    "old_2015.csv": [
        "2015-03-10",
        "20:55:44",
        6.8,
        -73.1,
        157,
        6.3,
        6.4,
        "SANTANDER",
        "LOS_SANTOS",
        20,
        0.2,
        90,
        1,
        1,
        2,
        "Revisado",
    ],
}


def test_load_both_systems_and_normalize_names(tmp_path):
    rows = ROWS
    for name, row in rows.items():
        with (tmp_path / name).open("w", newline="") as stream:
            csv.writer(stream).writerow(row)
    frame = load_catalog(tmp_path)
    assert set(frame.source_system) == {"old", "new"}
    assert set(frame.municipio) == {"LOS SANTOS"}
    assert set(frame.columns) >= {"datetime_utc", "lat", "lon", "depth_km", "mag", "mag_type"}
    assert frame.datetime_utc.notna().all()
    assert str(frame.datetime_utc.dt.tz) == "UTC"
    assert frame.loc[frame.source_system == "old", "mag"].item() == 6.4
    assert pd.api.types.is_numeric_dtype(frame.mag)


def test_reject_invalid_event_date(tmp_path):
    with (tmp_path / "new_2018.csv").open("w", newline="") as stream:
        csv.writer(stream).writerow(
            [
                "invalid",
                6,
                -73,
                150,
                3,
                "MLr",
                10,
                0.2,
                90,
                1,
                1,
                1,
                "Los Santos - Santander, Colombia",
                "",
                "",
                "",
                "manual",
            ]
        )
    with pytest.raises(ValueError, match="date"):
        load_catalog(tmp_path)


def test_exact_duplicate_events_do_not_double_counts(tmp_path):
    row = [
        "2018-03-01 00:49:05",
        6.8,
        -73.1,
        150,
        2.5,
        "MLr",
        10,
        0.3,
        80,
        1,
        1,
        2,
        "Los Santos - Santander, Colombia",
        "",
        "",
        "",
        "manual",
    ]
    with (tmp_path / "new_2018.csv").open("w", newline="") as stream:
        csv.writer(stream).writerows([row, row])
    frame = load_catalog(tmp_path)
    assert len(frame) == 1
    assert frame.attrs["duplicate_event_rows_removed"] == 1
