
import numpy as np
import polars as pl
import pytest

from ml_gcam import config
from ml_gcam.data import GcamDataset, Normalization

from tests import targets, datasets, double_loaded_datasets


def test_dataset_normalize_denormalize(targets):
    import einops

    source, split, samples, targets = targets
    dataset = GcamDataset(targets)
    dataset.with_normalization(Normalization(dataset.outputs))

    y_true = (
        targets.sort("experiment", "scenario_id", "region", "year")
        .select(*sorted(config.data.output_keys))
        .to_numpy()
    )

    y_true = einops.rearrange(
        y_true,
        "(samples dimensions) outputs -> samples dimensions outputs",
        dimensions=512,
        outputs=45,
    )
    y_pred = dataset.normalization.denormalize(dataset.normalization.normalize(y_true))
    assert np.allclose(
        y_pred, y_true, rtol=1e-03, atol=1e-03,
    ), f"{source} {split} y->normalize->denormalize changed"


def test_dataset_to_numpy(datasets):
    source, split, samples, dataset = datasets
    from ml_gcam.data.dataset import convert_targets_to_numpy

    targets = dataset.targets
    inputs, outputs = convert_targets_to_numpy(targets)
    assert np.all(inputs == dataset[:][0].numpy()), "inputs are not the same"
    assert np.allclose(dataset.normalization.normalize(outputs), dataset[:][1], rtol=1e-03, atol=1e-03), "outputs are not the same"

@pytest.mark.slow
def test_target_vs_dataset_outputs(datasets):
    """Outputs from GcamDataset are where we expect after converting to numpy."""
    source, split, samples, dataset = datasets

    sample_ids = dataset.targets.select("experiment", "scenario_id").unique().sort("experiment", "scenario_id")
    for i, (experiment, scenario_id) in enumerate(sample_ids.iter_rows()):

        value = (
            dataset.targets.filter(pl.col("experiment") == experiment)
            .filter(pl.col("scenario_id") == scenario_id)
            .select("region", "year", *sorted(config.data.output_keys))
            .sort("region", "year")
            .to_numpy()[:, 2:]
        )
        assert np.all(dataset.outputs[i] == value) , f"{experiment} {scenario_id} differs from expected"

def test_double_same_scenarios(double_loaded_datasets):
    source, split, samples, first, second = double_loaded_datasets

    first_ids = first.targets.select("experiment", "scenario_id").unique()
    second_ids = second.targets.select("experiment", "scenario_id").unique()
    joined = first_ids.join(second_ids, on=["experiment", "scenario_id"])
    assert len(first_ids) == len(joined), "first and second load had mismatch sample ids"

def test_double_same_outputs(double_loaded_datasets):
    source, split, samples, first, second = double_loaded_datasets

    assert np.all(first.outputs == second.outputs), "first and second have different outputs"

def test_double_same_inputs(double_loaded_datasets):
    source, split, samples, first, second = double_loaded_datasets

    assert np.all(first.inputs == second.inputs), "first and second have different inputs"

def test_double_same_items_input(double_loaded_datasets):
    source, split, samples, first, second = double_loaded_datasets

    assert np.all(first[:][0].numpy() == second[:][0].numpy()), "first and second have different inputs from __getitem__"

def test_double_same_items_outputs(double_loaded_datasets):
    source, split, samples, first, second = double_loaded_datasets

    assert np.all(first[:][1].numpy() == second[:][1].numpy()), "first and second have different outputs from __getitem__"
