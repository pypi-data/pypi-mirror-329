import numpy as np

from ml_gcam import config
from ml_gcam.evaluate import calculate_r2


def test_bad_r2():
    samples = 400
    dimensions = config.data.n_dimensions
    outputs = len(config.data.output_keys)

    zero = np.zeros((samples, dimensions, outputs))
    one = np.ones((samples, dimensions, outputs))
    scores = calculate_r2(zero, one)
    arr = scores.select(sorted(config.data.output_keys)).to_numpy()
    assert np.all(arr == 0.0), "r2 score should have been zero"


def test_perfect_r2():
    samples = 400
    outputs = len(config.data.output_keys)
    one = np.ones((samples, config.data.n_dimensions, outputs))
    scores = calculate_r2(one, one)
    perfect = scores.select(sorted(config.data.output_keys)).to_numpy()
    assert np.all(perfect == 1.0), "r2 should been 1.0"
