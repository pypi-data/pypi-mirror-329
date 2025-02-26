from pathlib import Path

import polars as pl

from ..data import GcamDataset, Normalization, Source, Split
from ..inference import Inference


def evaluate_renewable_adoption_vs_previous(
    targets_path: Path,
    train_source: str,
    checkpoint_path: Path,
    evaluate_on_test: bool = False,
) -> pl.DataFrame:
    train_set = GcamDataset.from_targets(
        save_path=targets_path,
        experiment=train_source,
        split=Split.TRAIN,
    )
    normalization = Normalization(outputs=train_set.outputs)
    train_set.with_normalization(normalization)
    dev_set = GcamDataset.from_targets(
        save_path=targets_path,
        experiment=Source.MIXED,
        split=[Split.TRAIN, Split.DEV],
    )
    dev_set.with_normalization(normalization)
    inference = (
        Inference.from_checkpoint(checkpoint_path)
        .eval_with(dev_set)
        .denormalize_with(train_set.normalization)
    )

    top = _top_regions(dev_set.targets)

    core = inference.y_true_df.filter(pl.col("region").is_in(top)).filter(
        pl.col("year").cast(pl.UInt16) <= 2050,
    )

    emulator = inference.y_pred_df.filter(pl.col("region").is_in(top)).filter(
        pl.col("year").cast(pl.UInt16) <= 2050,
    )

    columns = [
        pl.col("energy_supply_electricity_solar").alias("solar"),
        pl.col("energy_supply_electricity_wind").alias("wind"),
    ]

    core_med = (
        core.select("region", "year", *columns)
        .group_by("region", "year")
        .agg([pl.col("wind").median()])
    )

    emulator_med = (
        emulator.select("region", "year", *columns)
        .group_by("region", "year")
        .agg([pl.col("wind").median()])
    )
    core_med.join(emulator_med, on=["region", "year"], suffix="_pred").sort("wind")
    breakpoint()
    interact


def _top_regions(targets):
    column = "energy_supply_electricity_solar"
    return (
        targets.group_by("region")
        .agg(pl.col(column).sum().alias("solar"))
        .sort("solar", descending=True)[:8, "region"]
        .to_list()
    )
