from pathlib import Path

import polars as pl
import pytest

from ml_gcam import config
from ml_gcam.data import GcamDataset, Source, Split, load_targets

TARGETS = [
    (Source.MIXED, Split.TRAIN, 3264),
    (Source.MIXED, Split.DEV, 408),
]

@pytest.fixture(params=TARGETS, scope="session")
def targets(request):
    source, split, samples = request.param
    path = Path(config.paths.targets)
    targets = load_targets(path, [source], split)
    return (source, split, samples, targets)

def test_mixed_split_sizes(targets):
    source, split, samples, targets = targets
    scenarios = targets.select("experiment", "scenario_id").unique()
    experiments = (
        targets.select("experiment").unique().get_column("experiment").to_list()
    )

    for s, frac in [
        ("dawn_exp1_jr", 0.5),
        ("interp_random", 0.5),
    ]:
        assert s in experiments, f"missing {s}"
        source_scenarios = scenarios.filter(pl.col("experiment") == s)
        assert (
            len(source_scenarios) - (samples * frac)
        ) < 20, f"imbalanced samples. too many from {s}"


@pytest.fixture(params=config.mixed_fraction.fractions, scope="session")
def fractions(request):
    frac = request.param
    path = Path(config.paths.targets)
    mixed = GcamDataset.from_targets(save_path=path, experiment=Source.MIXED, split=Split.TRAIN, fraction_binary=float(frac))
    return frac, mixed

def test_frac_experiment_count(fractions):
    frac, dataset = fractions

    len_rand = dataset.targets.filter(pl.col("experiment") == "interp_random").select("experiment", "scenario_id").unique().height
    len_binary = dataset.targets.filter(pl.col("experiment") == "dawn_exp1_jr").select("experiment", "scenario_id").unique().height
    len_all = len_rand + len_binary

    pred_frac = (frac * len_all)
    diff = (len_binary - pred_frac)

    assert diff < 1, f"frac diff is {diff} from expected"

def test_frac_same_as_random(fractions):
    frac, dataset = fractions
    targets_path = Path(config.paths.targets)
    rand = GcamDataset.from_targets(targets_path, experiment=Source.RANDOM, split=Split.TRAIN)

    id_cols = ["experiment", "scenario_id"]
    mixed_keys = dataset.targets.select(id_cols).unique()
    rand_keys = rand.targets.select(id_cols).unique().sort(id_cols).sample(fraction=(1-frac), shuffle=False)
    frac_len = mixed_keys.height
    pred_len = rand_keys.height
    diff = pred_len - frac_len
    assert diff < 1, f"sampled random differs by {diff} from mixed fraction"

    joined = mixed_keys.join(rand_keys, on=id_cols)
    frac_len = mixed_keys.height
    joined_len = joined.height
    diff = joined_len - frac_len
    assert diff < 1, f"frac and random scenario ids differ by {diff}"
