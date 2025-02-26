from pathlib import Path

from ml_gcam import config
from ml_gcam.data import Source, load_targets


def test_parse_data_source():
    for source in config.data.sources:
        if config.data.sources[source].enabled:
            assert str(Source.from_str(source)) == source

def test_str_is_in():
    sources = [Source.BINARY, Source.SOBOL]
    assert "dawn_exp1_jr" in sources

def test_enum_passed_to_targets():
    targets_path = Path(config.paths.targets)
    targets = load_targets(targets_path, experiments=[Source.SOBOL], split="dev")
    assert len(targets) != 0

def test_static_methods():
    # Source.enabled()
    assert Source.MIXED not in Source.sampled()
    assert Source.SUPER not in Source.sampled()
    assert Source.BINARY in Source.sampled()
    assert Source.RANDOM in Source.sampled()
    assert Source.HYPERCUBE in Source.sampled()
    assert Source.RANDOM in Source.sampled()
    assert Source.SOBOL in Source.sampled()
