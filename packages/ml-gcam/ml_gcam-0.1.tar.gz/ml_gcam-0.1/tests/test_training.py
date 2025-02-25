from pathlib import Path

import pytest

from ml_gcam import config
from ml_gcam.data.dataset import GcamDataset
from ml_gcam.data.normalization import Normalization
from ml_gcam.emulator.model import ANN
from ml_gcam.inference import Inference


@pytest.fixture(
    params=config.data.train_sources, scope="session", ids=config.data.train_sources,
)
def datasets(request):
    source = request.param
    path = Path(config.paths.targets)
    train_set = GcamDataset.from_targets(path, experiment=source, split="train")
    dev_set = GcamDataset.from_targets(path, experiment=source, split="dev")
    return train_set, dev_set


@pytest.mark.skip("TODO")
def test_zero_model(datasets):
    dev_set, train_set = datasets

    model = ANN(
        in_size=len(config.data.input_keys),
        hidden_size=int(config.model.hidden_size),
        depth=int(config.model.depth),
        n_heads=config.data.n_dimensions,
        n_features=len(config.data.output_keys),
    )
    for param in model.parameters():
        param.data.zero_()
    inference = (
        Inference.from_model(model).eval_with(dev_set).denormalize_with(train_set.normalization)
    )
    scores = inference.scores
    arr = scores.select(config.data.output_keys).to_numpy()
    n_total = len(arr.flatten())
    n_zeros = len(arr[arr == 0])
    assert n_zeros == n_total, "datsaet multipled by all zeros yielded non-zero r2"


@pytest.mark.skip("TODO")
def test_identity_model(datasets):
    dev_set, train_set = datasets

    model = ANN(
        in_size=len(config.data.input_keys),
        hidden_size=int(config.model.hidden_size),
        depth=int(config.model.depth),
        n_heads=config.data.n_dimensions,
        n_features=len(config.data.output_keys),
    )
    for param in model.parameters():
        param.data.zero_()
    inference = (
        Inference.from_model(model).eval_with(dev_set).denormalize_with(train_set.normalization)
    )
    scores = inference.scores
    arr = scores.select(config.data.output_keys).to_numpy()
    n_total = len(arr.flatten())
    n_ones = len(arr[arr == 1])
    assert (
        n_ones == n_total
    ), f"dataset multipled by all ones yielded {n_total - n_ones} non-one r2"


def test_overfit():
    import os

    from ml_gcam.data.dataset import GcamDataset
    from ml_gcam.emulator.model import Arch
    from ml_gcam.evaluate import calculate_r2_aggs
    from ml_gcam.training.train import run_training

    #
    os.environ["ML_GCAM__TRAINING__EPOCHS"] = str(92)
    config.reload()

    checkpoint_path = Path(config.paths.repo) / "data/tests/checkpoint"
    path = Path(config.paths.targets)
    train_set = GcamDataset.from_targets(
        path, experiment="dawn_exp1_jr", split="train", samples=1,
    )
    normalization = Normalization(outputs=train_set.outputs)
    train_set.with_normalization(normalization)
    dev_set = GcamDataset.from_targets(path, experiment="dawn_exp1_jr", split="dev")
    dev_set.with_normalization(normalization)
    model = run_training(
        train_set,
        dev_set=dev_set,
        checkpoint_path=checkpoint_path,
        arch=Arch.DEEP,
    )

    run_inference = (
        Inference.from_model(model).eval_with(dev_set).denormalize_with(train_set.normalization)
    )
    check_inference = (
        Inference.from_checkpoint(checkpoint_path)
        .eval_with(dev_set)
        .denormalize_with(train_set.normalization)
    )
    run_scores = calculate_r2_aggs(run_inference.scores)
    checkpoint_scores = calculate_r2_aggs(check_inference.scores)

    for key, value in run_scores.items():
        assert (
            value == checkpoint_scores[key]
        ), f"{key} is different - run {value}, checkpoint {checkpoint_scores[key]}"

# def test_main():
#     calculate mean of all targets, then compare difference between mena and the predctions.
#     assert mean != prediction, "label mismatch, because it's predicting the mean"


