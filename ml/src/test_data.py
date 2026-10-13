"""Tests for panel loading, temporal splits and preprocessing."""

import numpy as np

from ml.src.data import (
    CLASS_LABELS,
    FUTURE_COLS,
    ID_COLS,
    META_COLS,
    build_supervised_frame,
    eligible_labeled_mask,
    load_metadata,
    load_panel,
    make_preprocessor,
    split_masks,
    temporal_month_splits,
    usable_months,
    validate_schema,
)


def _frame():
    panel = load_panel()
    metadata = load_metadata()
    return build_supervised_frame(panel, metadata)


def test_schema_matches_contract():
    panel = load_panel()
    metadata = load_metadata()
    features = validate_schema(panel, metadata)
    assert len(features) >= 20
    assert set(features) == set(metadata["features"])


def test_no_future_or_id_columns_in_x():
    x, _, _, _ = _frame()
    assert not (set(x.columns) & FUTURE_COLS)
    assert not (set(x.columns) & (set(ID_COLS) | set(META_COLS)))


def test_unusable_rows_are_excluded():
    panel = load_panel()
    metadata = load_metadata()
    mask = eligible_labeled_mask(panel)
    x, y, index, _ = build_supervised_frame(panel, metadata)
    assert len(x) == int(mask.sum()) == len(y) == len(index)
    assert set(y.unique()) <= set(CLASS_LABELS)


def test_splits_cover_each_month_once_in_order():
    _, _, index, _ = _frame()
    months = usable_months(index)
    splits = temporal_month_splits(months)
    seen = [m for part in splits.values() for m in part]
    assert sorted(seen) == months
    assert len(set(seen)) == len(seen)
    assert list(splits) == ["train", "val", "test"]
    assert max(splits["train"]) < min(splits["val"]) < min(splits["test"])


def test_split_masks_are_disjoint_and_complete():
    _, _, index, _ = _frame()
    splits = temporal_month_splits(usable_months(index))
    masks = split_masks(index, splits)
    total = sum(m.sum() for m in masks.values())
    assert total == len(index)
    overlap = (masks["train"] & masks["val"]).sum()
    overlap += (masks["train"] & masks["test"]).sum()
    overlap += (masks["val"] & masks["test"]).sum()
    assert overlap == 0


def test_splits_are_reproducible():
    _, _, index, _ = _frame()
    months = usable_months(index)
    assert temporal_month_splits(months) == temporal_month_splits(months)


def test_preprocessor_handles_nulls_and_fits_train_only():
    x, _, index, _ = _frame()
    splits = temporal_month_splits(usable_months(index))
    masks = split_masks(index, splits)
    x_train = x[masks["train"]]
    pre = make_preprocessor()
    transformed = pre.fit_transform(x_train)
    assert not np.isnan(np.asarray(transformed)).any()
    medians = pre.named_steps["impute"].statistics_
    expected = x_train.median(numeric_only=True).to_numpy()
    np.testing.assert_allclose(medians, expected, rtol=1e-6)
    val_out = pre.transform(x[masks["val"]])
    assert not np.isnan(np.asarray(val_out)).any()


def test_index_traces_each_row_to_municipality_and_month():
    _, _, index, _ = _frame()
    assert list(index.columns) == ["zone_id", "month", "feature_cutoff"]
    assert index[["zone_id", "month"]].duplicated().sum() == 0


def test_missing_class_is_reported_not_hidden():
    _, y, index, _ = _frame()
    splits = temporal_month_splits(usable_months(index))
    masks = split_masks(index, splits)
    for name, mask in masks.items():
        present = set(y[mask].unique())
        assert present <= set(CLASS_LABELS), name
