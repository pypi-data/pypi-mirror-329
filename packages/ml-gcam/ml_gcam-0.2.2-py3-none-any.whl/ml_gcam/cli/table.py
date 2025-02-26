import time
from pathlib import Path
from typing import Optional

import click

from .. import config, logger
from ..cli.options import (
    force,
    save_or_print,
    save_path,
    table_format,
    targets_path,
    validate_force,
)


@click.group()
def cli():
    """Table of results."""


@click.option(
    "-d",
    "--dir_path",
    "dir_path",
    required=True,
    type=Path,
)
@table_format()
@save_path(path_help="/path/to/sensitivity.tex output", suffix=".tex", required=False)
@force()
@cli.command("table:sensitivity")
def table_sensitivity(
    dir_path: Path,
    table_format: str,
    save_path: Path,
    force: bool,
):
    """Plot cartesian product of sensitivity experiments."""
    from ..table import sensitivity_table

    validate_force(save_path, force=force)
    table = sensitivity_table(dir_path)
    save_or_print(table, table_format, save_path)


@click.option(
    "-s",
    "--score_path",
    type=click.Path(dir_okay=False, exists=True, readable=True, path_type=Path),
    help="/path/to//sample-size/scores.csv",
    required=True,
    default=Path(config.paths.data) / "processed/sample_size/r2_scores.csv",
)
@table_format()
@save_path(path_help="path to save table.tex", suffix=".tex", required=False)
@force()
@cli.command("table:cartesian")
def table_cartesian(
    score_path: Path,
    table_format: str,
    save_path: Optional[Path],
    force: bool,
):
    """Create latex table of cartesian experiments."""
    from ..table import cartesian

    validate_force(save_path, force)

    start_time = time.perf_counter()
    table = cartesian(score_path)
    save_or_print(table, table_format, save_path)
    end_time = time.perf_counter()
    logger.info(f"saved {save_path} [{end_time - start_time:.2f} seconds]")


@click.option(
    "-s",
    "--score_path",
    type=click.Path(dir_okay=False, exists=True, readable=True, path_type=Path),
    help="/path/to//sample-size/scores.csv",
    required=True,
    default=Path(config.paths.data) / "processed/sample_size/r2_scores.csv",
)


@cli.command("table:quantities")
@table_format()
@save_path(path_help="path to save table.tex", suffix=".tex", required=False)
@force()
def table_outputs(table_format: str, force: bool, save_path: Optional[Path]):
    """Create latex table of experiment outputs."""
    from ..table import quantites 

    validate_force(save_path, force)

    start_time = time.perf_counter()
    table = quantities()
    save_or_print(table, table_format, save_path)
    end_time = time.perf_counter()
    logger.info(f"saved {save_path} [{end_time - start_time:.2f} seconds]")



@table_format()
@force()
@save_path(path_help="path to save inputs_table.tex", suffix=".tex", required=False)
@cli.command("table:inputs")
def table_inputs(table_format: str, force: bool, save_path: Path):
    """Create latex table of experiment inputs."""
    from ..table import inputs

    validate_force(save_path, force)

    start_time = time.perf_counter()
    table = inputs()
    save_or_print(table, table_format, save_path)
    end_time = time.perf_counter()
    logger.info(f"saved {save_path} [{end_time - start_time:.2f} seconds]")



@targets_path()
@table_format()
@force()
@save_path(path_help="path to save datasets_table.tex", suffix=".tex", required=False)
@cli.command("table:datasets")
def table_datasets(targets_path: Path, table_format: str, force: bool, save_path: Path):
    """Create latex table of experiment datasets."""
    from ..table import datasets

    validate_force(save_path, force)

    start_time = time.perf_counter()
    table = datasets(targets_path)
    breakpoint()
    save_or_print(table, table_format, save_path)
    end_time = time.perf_counter()
    logger.info(f"saved {save_path} [{end_time - start_time:.2f} seconds]")
