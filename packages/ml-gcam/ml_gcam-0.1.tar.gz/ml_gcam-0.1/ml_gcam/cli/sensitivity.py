from pathlib import Path
from typing import Optional

import click

from .. import config, logger
from ..cli.options import (
    force,
    save_path,
    train_source,
    dev_source,
    validate_force,
    checkpoint_path,
    targets_path,
)

from ..data import NormStrat, Source


@click.group()
def cli():
    """SALib Sensitivity Analysis."""


@click.option(
    "-n",
    "--normalization-strategy",
    "strategy",
    help="normalization strategy used to train the emulator",
    type=click.Choice(["z_score", "min_max", "robust"]),
    default="z_score",
    required=True,
)
@click.option(
    "-s",
    "--save_directory",
    type=str,
    required=True,
)
@click.option(
    "-l",
    "--level",
    type=click.Choice(["vi", "dgsm"]),
    help="calculate dgsm => True, calculate vi => False",
    required=True,
)   
@targets_path()
@train_source()
@checkpoint_path()
@cli.command("evaluate:sensitivity")
def compare_dgsm(
        targets_path, 
        train_source, 
        checkpoint_path: Path = None, 
        save_directory: Path = None, 
        level: str = None, 
        strategy = 'z_score', 
        sensitivity_norm: str = 'sigma'
):
    """Compare dgsm/vi between GCAM core and Emulator"""
    from ..evaluate import dgsm_sensitivity_compare

    dgsm_sensitivity_compare(
            targets_path, 
            train_source, 
            checkpoint_path, 
            save_directory, 
            level, 
            NormStrat.from_str(strategy), 
    )


@cli.command("plot:sensitivity")
@click.option(
    "-d",
    "--dir_path",
    "dir_path",
    help="path/to/vi/*_samples",
    required=True,
    type=Path,
)
@click.option(
    "-c",
    "--cumulative",
    "cumulative",
    is_flag=True,
    required=True,
    default=False,
    type=bool,
)
@click.option(
    "-k",
    "--kde",
    "kde",
    is_flag=True,
    required=True,
    default=False,
    type=bool,
)
@force()
@train_source()
@save_path(path_help="path to save figure.png", suffix=".png")
def plot_sensitivity(
        dir_path: Path,
        cumulative: bool,
        kde: bool,
        save_path: str,
        force: bool,
        train_source: str,
    ):
    """plot sensitivity between core and emulator"""
    from ..plot import sensitivity_one_to_one

    validate_force(save_path, force)
    world_paths = [world for world in sorted(dir_path.iterdir())]
    if cumulative:
        fig = sensitivity_one_to_one(
            world_paths,
            cumulative,
            kde,
            str(train_source),
        )
        fig.savefig(save_path, dpi=300)
        logger.info(f"saved: {save_path}")
    else:
        for i, file in enumerate(world_paths):
            fig = sensitivity_one_to_one(
                [file],
                cumulative,
                kde,
                str(train_source),
            )
            name = file.name.split(":")[1].split(".")[0]
            fig.savefig(save_path.parent / f"{name}.png", dpi=300)
            logger.info(f"saved: {save_path}")


@click.option(
    "-s",
    '--sensitivity-path',
    help="/path/to/{level}/{train_source}",
    type=click.Path(dir_okay=True, readable=True, exists=True, path_type=Path),
    required=True
)
@force()
@save_path(path_help="path to save figure.png", suffix=".png")
@cli.command("plot:sensitivity-heatmap")
def sensitivity_heatmap(
    sensitivity_path: Path,
    force: bool,
    save_path: Path,
):
    """Plot the heatmaps for sensitivity"""
    from ..plot import sensitivity_heatmaps

    validate_force(save_path, force)
    fig = sensitivity_heatmaps(sensitivity_path)
    fig.savefig(save_path, dpi=300, bbox_inches="tight")
    logger.info(f"saved: {save_path}")



