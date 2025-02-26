from collections import namedtuple
from pathlib import Path

import pytest

from ml_gcam import config
from ml_gcam.data import GcamDataset, Normalization, Source, Split, load_targets

Target = namedtuple("Target", ["sample", "split", "samples"])
TARGETS = [
    Target("dawn_exp1_jr", "train", 3264),
    Target("dawn_exp1_jr", "dev", 408),
    Target("dawn_exp1_jr", "test", 408),
    Target("interp_random", "train", 3264),
    Target("interp_random", "dev", 408),
    Target("interp_random", "test", 408),
    Target("interp_hypercube", "train", 3264),
    Target("interp_hypercube", "dev", 408),
    Target("interp_hypercube", "test", 408),
    Target("interp_sobol", "dev", 2047),
    Target("mixed", "train", 3264),
    Target("mixed", "dev", 408),
    Target("super", "train", 3264),
    Target("super", "dev", 408),
]
TARGET_IDS = [
    "dawn|train",
    "dawn|dev",
    "dawn|test",
    "random|train",
    "random|dev",
    "random|test",
    "hypercube|train",
    "hypercube|dev",
    "hypercube|test",
    "sobol|dev",
    "mixed|train",
    "mixed|dev",
    "super|train",
    "super|dev",
]

@pytest.fixture(params=TARGETS, scope="session", ids=TARGET_IDS)
def targets(request):
    source, split, samples = request.param
    path = Path(config.paths.targets)
    targets = load_targets(path, [source], split)
    return (source, split, samples, targets)


@pytest.fixture(params=[(None, None, None)], scope="session", ids=["all|all"])
def full_targets(request):
    source, split, samples = request.param
    path = Path(config.paths.targets)
    targets = load_targets(path, experiments=Source.sampled(), split=Split.all())
    return (source, split, samples, targets)

@pytest.fixture(params=TARGETS, scope="session", ids=TARGET_IDS)
def datasets(request):
    source, split, samples = request.param
    path = Path(config.paths.targets)
    dataset = GcamDataset.from_targets(save_path=path, experiment=source, split=split)
    dataset.with_normalization(Normalization(dataset.outputs))
    return (source, split, samples, dataset)



@pytest.fixture(params=TARGETS, scope="session", ids=TARGET_IDS)
def double_loaded_targets(request):
    source, split, samples = request.param
    path = Path(config.paths.targets)
    first = load_targets(path, [source], split)
    second = load_targets(path, [source], split)
    return (source, split, samples, first, second)

@pytest.fixture(params=TARGETS, scope="session", ids=TARGET_IDS)
def double_loaded_datasets(request):
    source, split, samples = request.param
    path = Path(config.paths.targets)
    first = GcamDataset.from_targets(save_path=path, experiment=source, split=split)
    first.with_normalization(Normalization(first.outputs))
    second = GcamDataset.from_targets(save_path=path, experiment=source, split=split)
    second.with_normalization(Normalization(second.outputs))
    return (source, split, samples, first, second)

