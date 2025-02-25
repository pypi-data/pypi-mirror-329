import os
from pathlib import Path

import numpy as np
import polars as pl
import pytest

from ml_gcam import config
from ml_gcam.data import load_targets
from tests import full_targets, targets, double_loaded_targets


def test_single_splits(targets):
    source, split, samples, targets = targets

    splits = targets.select("split").unique().get_column("split").to_list()
    assert len(splits) == 1, f"multiple splits in {source} {split} set"
    assert split in splits, f"target does not contain {split}"


@pytest.mark.skip("not sure if this is strictly an error")
def test_mean_is_not_zero(targets):
    source, split, samples, targets = targets

    mean_df = (
        targets.group_by("region", "year")
        .agg([pl.col(c).mean().alias(c) for c in sorted(config.data.output_keys)])
        .sort("region", "year")
    )
    mean_arr = mean_df.select(sorted(config.data.output_keys)).to_numpy()

    n_zeros = len(mean_arr[mean_arr == 0].flatten())
    total = len(mean_arr.flatten())
    frac = n_zeros / total
    assert (
        n_zeros == 0
    ), f"{n_zeros} targets have mean of 0 ({frac * 100:.2f}% of {total})"


@pytest.mark.skip("not sure if this is strictly an error")
def test_std_is_not_zero(targets):
    source, split, samples, targets = targets

    std_df = (
        targets.group_by("region", "year")
        .agg([pl.col(c).std().alias(c) for c in sorted(config.data.output_keys)])
        .sort("region", "year")
    )
    std_arr = std_df.select(sorted(config.data.output_keys)).to_numpy()

    n_zeros = len(std_arr[std_arr == 0].flatten())
    total = len(std_arr.flatten())
    frac = n_zeros / total
    assert (
        n_zeros == 0
    ), f"{n_zeros} targets have std. dev. of 0 ({frac * 100:.2f}% of {total})"

    # zeros = np.where(std_arr == 0)
    # elements = list(zip(zeros[0], zeros[1]))
    # collect = []
    # for row, col in elements:
    #     col_name = sorted(config.data.output_keys)[col]
    #     region, year = std_df.slice(row, 1).select("region", "year").row(0)
    #     collect.append({"output": col_name, "region": region, "year": year})
    #
    # zero_df = pl.DataFrame(collect)
    #
    # zero_df.group_by("output").count().sort("count")
    # zero_df.group_by("region").count().sort("count")
    # zero_df.group_by("year").count().sort("count")


def test_split_sample_size(targets):
    source, split, samples, targets = targets
    scenarios = targets.select("experiment", "scenario_id").unique()
    found, _ = scenarios.shape
    assert found == samples, f"{found} scenarios, should be {samples}"


def test_source_in_targets(targets):
    source, split, samples, targets = targets
    sources = targets.select("experiment").unique().get_column("experiment").to_list()
    if source not in ["mixed", "super"]:
        assert source in sources, f"{source} {split} missing {source}"
    elif source == "mixed":
        for s in ["dawn_exp1_jr", "interp_random"]:
            assert s in sources, f"{source} {split} missing {s}"
    elif source == "super":
        for s in ["dawn_exp1_jr", "interp_random", "interp_hypercube"]:
            assert s in sources, f"{source} {split} missing {s}"


def test_output_columns(targets):
    source, split, samples, targets = targets
    for target in config.data.output_keys:
        assert target in targets.columns, f"{source} {split} missing {target} column"


def test_region_columns(targets):
    source, split, samples, targets = targets
    regions = targets.select("region").unique().get_column("region").to_list()
    for region in config.data.region_keys:
        assert region in regions, f"{source} {split} missing {region} rows"


def test_year_columns(targets):
    source, split, samples, targets = targets
    years = targets.select("year").unique().get_column("year").to_list()
    for year in config.data.year_keys:
        assert year in years, f"{source} {split} missing {year} rows"


def test_input_value_range(targets):
    source, split, samples, targets = targets
    inputs = targets.select(*config.data.input_keys).unique().to_numpy()
    assert not inputs[inputs > 1.0].any(), "found input greater than zero"
    assert not inputs[inputs < 0.0].any(), "found input less than zero"


def test_mixed_and_super_split_sizes(targets):
    source, split, samples, targets = targets
    if source not in ["mixed", "super"]:
        return
    scenarios = targets.select("experiment", "scenario_id").unique()
    experiments = (
        targets.select("experiment").unique().get_column("experiment").to_list()
    )
    if source == "mixed":
        for s, frac in [
            ("dawn_exp1_jr", 0.5),
            ("interp_random", 0.5),
        ]:
            assert s in experiments, f"missing {s}"
            source_scenarios = scenarios.filter(pl.col("experiment") == s)
            assert (
                len(source_scenarios) - (samples * frac)
            ) < 20, f"imbalanced samples. too many from {s}"
    elif source == "super":
        for s, frac in [
            ("dawn_exp1_jr", 0.2),
            ("interp_random", 0.4),
            ("interp_hypercube", 0.4),
        ]:
            assert s in experiments, f"missing {s}"
            source_scenarios = scenarios.filter(pl.col("experiment") == s)
            assert (
                len(source_scenarios) - (samples * frac)
            ) < 20, f"imbalanced samples. too many from {s}"


@pytest.mark.slow
def test_full_targets(full_targets):
    source, split, samples, targets = full_targets
    splits = targets.select("split").unique().get_column("split").to_list()
    assert len(splits) == 3, "not all splits in targets"

    experiments = (
        targets.select("experiment").unique().get_column("experiment").to_list()
    )
    sources = [s["key"] for key, s in config.data.sources.items() if s["enabled"] and s["new_samples"]]
    for name in sources:
        assert name in experiments, f"full targets missing {name} source"

@pytest.mark.slow
def test_multiple_target_loads(double_loaded_targets):
    source, split, samples, first, second = double_loaded_targets

    first_uniq = first.select("experiment", "scenario_id").unique()
    second_uniq = second.select("experiment", "scenario_id").unique()
    len_first = len(first_uniq)
    len_second = len(second_uniq)
    assert len_first == len_second, "targets should have same count of unique scenarios"

    first_ids = first_uniq.select(
        (pl.col("experiment") + "-" + pl.col("scenario_id").cast(pl.String)).alias("id"),
    )["id"]
    second_ids = second_uniq.select(
        (pl.col("experiment") + "-" + pl.col("scenario_id").cast(pl.String)).alias("id"),
    )["id"]

    difference = set(first_ids) - set(second_ids)
    n_difference = len(difference)
    assert (
        n_difference == 0
    ), f"{n_difference} ids exist in first that are not in second ({difference})"

    difference = set(second_ids) - set(first_ids)
    n_difference = len(difference)
    assert (
        n_difference == 0
    ), f"{n_difference} ids exist in second that are not in first ({difference})"


def test_old_vs_new_outputs():
    os.environ["ML_GCAM__PATHS__TARGETS"] = str(
        Path(config.paths.data) / "targets/targets.parquet",
    )
    config.reload()
    new = load_targets(Path(config.paths.targets))

    os.environ["ML_GCAM__PATHS__TARGETS"] = str(
        Path(config.paths.data) / "targets/features.parquet",
    )
    config.reload()
    old = load_targets(Path(config.paths.targets))

    old_data = (
        old.sort("experiment", "scenario_id", "split", "region", "year")
        .select(sorted(config.data.output_keys))
        .to_numpy()
    )
    new_data = (
        new.sort("experiment", "scenario_id", "split", "region", "year")
        .select(sorted(config.data.output_keys))
        .to_numpy()
    )

    import numpy as np

    assert np.allclose(
        old_data, new_data, rtol=1e-03, atol=1e-03,
    ), "old has different output values as new"

def test_sample_from_env():
    assert "sample_size" in config
    assert "total_samples" in config.sample_size
    total_samples = int(config.sample_size.total_samples)
    assert total_samples < 4096


def test_total_sample_size_less_than_train_source():
    train_source = config.training.train_source
    targets = load_targets(Path(config.paths.targets), [train_source], "train")
    keys = targets.select("experiment", "scenario_id").unique()
    samples_in_train = len(keys)
    for fraction in config.sample_size.splits:
        sample_size = int(int(config.sample_size.total_samples) * fraction)
        assert (
            sample_size <= samples_in_train
        ), f"{sample_size=} is more than {samples_in_train=} for {train_source}"


def test_input_mean_is_0_5(targets):
    source, split, samples, targets = targets
    inputs = targets.select(config.data.input_keys).unique().to_numpy()
    assert len(inputs) == samples
    half = np.full(12, 0.5)
    mean = inputs.mean(axis=0)
    assert np.allclose(
        mean, half, rtol=0.05, atol=0.05,
    ), "input means not 0.5 for split"


