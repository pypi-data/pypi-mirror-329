import os
from pathlib import Path

import pytest

from ml_gcam import config

PATHS_MUST_EXIST = [
    "dist",
    "figures",
    "core",
    "repo",
    "data",
    # "extract.gcamreader_outputs",
    # "extract.save",
    # "interpolation",
    "targets",
    "scenarios",
    # "tensorboard",
    "checkpoint",
]


@pytest.mark.parametrize("config_name", PATHS_MUST_EXIST)
def test_paths_exist_and_readable(config_name):
    assert (
        config_name in config.paths
    ), f"'{config_name}' is not a key in config.paths. update $ENV, .env or config.toml"
    name = config.paths[config_name]
    path = Path(name)
    assert path.exists(), f"'{path}' does not exist. update $ENV, .env or config.toml"
    assert os.access(path, os.R_OK), f"{path} is not readable"


def test_modify_and_reload():
    import os

    debug = bool(int(config.debug))
    project = config.project

    os.environ["ML_GCAM__DEBUG"] = "0" if debug else "1"
    config.reload()
    assert debug != bool(int(config.debug))
    assert project == config.project


def test_wandb():
    assert (
        "WANDB_API_KEY" in os.environ
    ), "wandb api key needs to be set via $ENV or .env"


TRAINING_VARS = [
    "train_source",
    "dev_source",
    "epochs",
    "batch_size",
    "learning_rate",
    "metric_freq",
    "evaluate_on_test",
    "samples",
]


@pytest.mark.parametrize("config_name", TRAINING_VARS)
def test_training(config_name):
    assert config_name in config.training, f"missing {config_name} in config.training"


def test_training_set():
    assert config.training.train_source in config.data.train_sources


def test_dev_source():
    assert config.training.dev_source in config.data.dev_sources


def test_hyperparameters():
    assert str(config.training.epochs).isdigit()
    assert str(config.training.metric_freq).isdigit()
    assert str(config.training.samples).isdigit()
    assert str(config.training.batch_size).isdigit()
    assert str(config.model.depth).isdigit()
    assert str(config.model.hidden_size).isdigit()
    assert float(config.training.learning_rate) < 1


def test_data_targets():
    parent = Path(config.paths.targets)
    assert parent.suffix == ".parquet", "targets need to be a .parquet filetype"


@pytest.mark.skip(reason="random_seed is 42 by default. change for production.")
def test_random_seed():
    assert "random_seed" in config, "set config.random_seed when going to production"


@pytest.mark.skip(
    reason="idk if we need a config for the latest model or if the cli should have a param",
)
def test_model_save_targets():
    parent = Path(config.paths.model.latest)
    assert (
        ".safetensors" in [c.suffix for c in parent.iterdir()]
    ), "config.paths.model.latest does not contain accelerate checkpoint file (missing .safetensor)"
    checkpoint = Path(config.paths.model.checkpoint)
    assert os.access(
        checkpoint, os.W_OK,
    ), f"cannot write to checkpoint path {checkpoint}"


def test_data_inputs_and_outputs():
    assert len(config.data.region_keys) * len(config.data.years) == 512
    assert len(config.data.regions) * len(config.data.years.keys()) == 512
    inputs = [
        "back",
        "bio",
        "ccs",
        "elec",
        "emiss",
        "energy",
        "ff",
        "nuc",
        "solarS",
        "solarT",
        "windS",
        "windT",
    ]
    for row in config.data.inputs:
        assert row in inputs

    regions = [
        "Africa_Eastern",
        "Africa_Northern",
        "Africa_Southern",
        "Africa_Western",
        "Argentina",
        "Australia_NZ",
        "Brazil",
        "Canada",
        "Central America and Caribbean",
        "Central Asia",
        "China",
        "Colombia",
        "EU-12",
        "EU-15",
        "Europe_Eastern",
        "Europe_Non_EU",
        "European Free Trade Association",
        "India",
        "Indonesia",
        "Japan",
        "Mexico",
        "Middle East",
        "Pakistan",
        "Russia",
        "South Africa",
        "South America_Northern",
        "South America_Southern",
        "South Asia",
        "South Korea",
        "Southeast Asia",
        "Taiwan",
        "USA",
    ]
    for row in config.data.regions:
        assert row in regions

    for key in config.data.region_keys:
        assert key in regions

    # these are what we decided to include in the paper
    checklist = [
        "energy_demand_elec_transport",
        "energy_demand_elec_industry",
        "energy_demand_elec_building",
        "energy_demand_fuel_hydrogen",
        "energy_demand_fuel_fossil_transport",
        "energy_demand_fuel_fossil_industry",
        "energy_demand_fuel_fossil_building",
        # "energy_demand_fuel_biomass_transport",
        "energy_demand_fuel_biomass_industry",
        "energy_demand_fuel_biomass_building",
        "energy_price_electricity",
        "energy_price_coal",
        "energy_price_gas",
        "energy_price_oil",
        "energy_supply_electricity_coal",
        "energy_supply_electricity_oil",
        "energy_supply_electricity_gas",
        "energy_supply_electricity_solar",
        "energy_supply_electricity_wind",
        "energy_supply_electricity_biomass",
        "energy_supply_electricity_nuclear",
        "energy_supply_electricity_other",
        "energy_supply_primary_coal",
        "energy_supply_primary_oil",
        "energy_supply_primary_gas",
        "energy_supply_primary_solar",
        "energy_supply_primary_wind",
        "energy_supply_primary_biomass",
        "energy_supply_primary_nuclear",
        "energy_supply_primary_other",
        "land_demand_feed",
        "land_demand_food",
        "land_price_biomass",
        "land_price_forest",
        "land_allocation_forest",
        "land_allocation_biomass",
        "land_allocation_pasture",
        "land_allocation_grass_shrub",
        "land_allocation_other",
        "land_production_forest",
        "land_production_biomass",
        "land_production_pasture",
        "land_production_grass_shrub",
        "land_production_other",
        "water_demand_crops",
        "water_demand_electricity",
    ]

    for key in checklist:
        assert (
            key in config.data.output_keys
        ), f"{key} from output checklist not in config.data.output_keys"
