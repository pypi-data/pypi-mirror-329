import time
from pathlib import Path

import click
import polars as pl

from .. import config, logger
from ..cli.options import (
    checkpoint_path,
    dev_source,
    force,
    save_or_print,
    save_path,
    table_format,
    targets_path,
    train_source,
    validate_force,
)
from ..data import GcamDataset, Source, Split, NormStrat


@click.group()
def cli():
    pass


@cli.command("debug:targets")
def main():
    pass


@cli.command("debug:time")
@click.option(
    "-n",
    "--num-batches",
    type=int,
    help="number of batches to evaluate",
    required=True,
    default=200,
)
@checkpoint_path()
def time_trial(
    checkpoint_path: Path,
    num_batches: int = 200,
):
    ''' Investigate zero sensitivity for nuclear '''
    from ..emulator import Arch
    from accelerate import Accelerator
    import torch
    from scipy.stats import qmc

    start_time = time.perf_counter()
    arch = Arch.from_str(config.model.arch)
    model = arch.init_model()

    accelerator = Accelerator()
    model = accelerator.prepare(model)
    accelerator.load_state(checkpoint_path)
    end_time = time.perf_counter()
    logger.info(f"loading model [{end_time - start_time:.2f} seconds]")
    
    sampler = qmc.LatinHypercube(d=12)
    bits = torch.Tensor(sampler.random(n=200)).to("cuda:0")
    
    
    start_time = time.perf_counter()
    for _ in range(num_batches):
        _ = model(bits)
    end_time = time.perf_counter()
    logger.info(f"evaluation for {200*num_batches} data points [{end_time - start_time:.2f} seconds]")


@cli.command("debug:nuclear")
@targets_path()
@dev_source()
def debug_nuclear(
    targets_path: Path,
    dev_source: Source,
):
    ''' Investigate zero sensitivity for nuclear '''
    from ..debug import debug_nuclear

    dataset = GcamDataset.from_targets(
        targets_path,
        experiment=dev_source,
        split=[Split.TRAIN, Split.DEV, Split.TEST],
    ).targets

    debug_nuclear(dataset)



@targets_path()
@checkpoint_path()
@train_source()
@dev_source()
@table_format()
@save_path(required=False)
@force()
@cli.command("debug:negative-scores")
def negative_scores(
    targets_path: Path,
    checkpoint_path: Path,
    train_source: Source,
    dev_source: Source,
    table_format: str,
    save_path: Path,
    force: bool,
):
    """Calculate negative region, year, output combinations from checkpoint."""
    from ..debug import plot_dimensions_with_negative_scores
    from ..evaluate.metrics import dimensions_with_negative_scores
    from ..inference import Inference

    validate_force(save_path, force)
    train_set = GcamDataset.from_targets(
        targets_path,
        experiment=train_source,
        split=Split.TRAIN,
    )
    dev_set = GcamDataset.from_targets(
        targets_path,
        experiment=dev_source,
        split=Split.DEV,
    )
    inference = (
        Inference.from_checkpoint(checkpoint_path)
        .use_dataset(dev_set)
        .denormalize_with(train_set)
    )
    table = dimensions_with_negative_scores(inference.scores)
    total = table.height
    fraction_col = (pl.len() / total * 100).alias("fraction")
    table.group_by("region").agg([fraction_col]).sort("fraction")
    table.group_by("year").agg([fraction_col]).sort("fraction")
    table.group_by("output").agg([fraction_col]).sort("fraction")
    # breakpoint()
    save_or_print(table, table_format, save_path)
    # train_set.targets.join(dev_set.targets, on=config.data.input_keys).shape[0] == 0
    # dev_set.targets.select("experiment", "scenario_id").unique()
    fig = plot_dimensions_with_negative_scores(table)
    figure_path = Path(config.paths.dist) / "figures/negative_scores_debug.png"
    fig.savefig(figure_path)
    logger.debug(f"saved {figure_path}")


@cli.command("debug:save-old-targets")
def save_old_targets():
    """I want to know if features.csv and targets.parquet are close to the same."""
    old_targets = pl.read_csv(
        Path(config.paths.data) / "meta/features.csv",
        separator="|",
    )
    old_scenarios = pl.read_csv(
        Path(config.paths.data) / "meta/scenarios.csv",
        separator="|",
    )
    old_inputs = (
        old_scenarios["encoding"]
        .str.strip_chars_start("[")
        .str.strip_chars_end("]")
        .str.split(",")
        .list.to_struct(fields=sorted(config.data.input_keys))
        .struct.unnest()
    )
    old_scenarios = pl.concat([old_scenarios, old_inputs], how="horizontal")
    old = old_scenarios.join(old_targets, on=["scenario", "experiment"])

    to_save = old.select(
        pl.col("experiment"),
        pl.col("scenario_id"),
        pl.col("region"),
        pl.col("year"),
        pl.col("split"),
        *sorted(config.data.output_keys),
        *sorted(config.data.input_keys),
    )

    to_save.write_parquet(
        Path(config.paths.data) / "targets/features.parquet",
        pyarrow_options={"partition_cols": ["experiment", "split"]},
    )


@cli.command("debug:new-vs-old")
def new_vs_old_targets():
    """I want to know if features.csv and targets.parquet are close to the same."""
    pass


@cli.command("debug")
def debug():
    breakpoint()
    interact
    pl.read_csv(
        Path(config.paths.repo)
        / "data/raw/query_outputs/dawn_exp1_jr/sample/elec_gen_by_subsector.csv",
        separator="|",
    )


@cli.command("debug:checkpoint")
@checkpoint_path()
@train_source()
@dev_source()
@targets_path()
def debug_checkpoint(
    checkpoint_path: Path,
    train_source: str,
    dev_source: str,
    targets_path: Path,
):
    """Load and create r2 scores for a checkpoint."""
    from ..data import GcamDataset, Split
    from ..evaluate import calculate_r2_aggs
    from ..inference import Inference

    logger.info("evaluating checkpoint")
    start_time = time.perf_counter()

    train_set = GcamDataset.from_targets(
        targets_path,
        train_source,
        Split.TRAIN,
        fraction_binary=0.0,
    )
    dev_set = GcamDataset.from_targets(targets_path, dev_source, Split.DEV)

    inference = (
        Inference.from_checkpoint(checkpoint_path)
        .use_dataset(dev_set)
        .denormalize_with(train_set)
    )

    aggs = calculate_r2_aggs(inference.scores)
    for key, value in aggs.items():
        logger.info(f"{key}: {value}")

    end_time = time.perf_counter()
    logger.info(f"evaluating done [{end_time - start_time:.2f} seconds]")
    breakpoint()


@click.option(
    "-s",
    "--score_path",
    type=click.Path(dir_okay=False, exists=True, readable=True, path_type=Path),
    help="/path/to/fraction_binary_r2.csv",
    required=True,
    default=Path(config.paths.data) / "processed/fraction_binary_r2.csv",
)
@table_format()
@save_path(path_help="/path/to/sensitivity.tex output", suffix=".tex", required=False)
@force()
@cli.command("debug:negative-fraction-binary")
def negative_fraction_binary(
    score_path: Path,
    table_format: str,
    save_path: Path,
    force: bool,
):
    from ..table.table import fraction_binary_negative_values

    validate_force(save_path, force)

    table = fraction_binary_negative_values(score_path)
    save_or_print(table, table_format, save_path)
