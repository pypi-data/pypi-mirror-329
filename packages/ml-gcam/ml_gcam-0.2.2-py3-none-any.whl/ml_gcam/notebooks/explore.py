import marimo

__generated_with = "0.3.12"
app = marimo.App()


@app.cell
def __():
    from pathlib import Path

    import marimo as mo
    import matplotlib.pyplot as plt
    import polars as pl
    import seaborn as sns

    from ml_gcam import config
    from ml_gcam.data import NormStrat
    from ml_gcam.data.dataset import GcamDataset
    from ml_gcam.data.targets import load_targets

    return (
        GcamDataset,
        NormStrat,
        Path,
        config,
        load_targets,
        mo,
        pl,
        plt,
        sns,
    )


@app.cell
def __(Path, config, load_targets):
    targets_path = Path(config.paths.targets)
    targets = load_targets(
        save_path=targets_path,
        experiments=["dawn_exp1_jr", "interp_random"],
        split="train",
    )
    # dataset = GcamDataset(targets=targets, strategy=NormStrat.Z_SCORE)
    return targets, targets_path


@app.cell
def __(config, mo):
    dropdown = mo.ui.dropdown(
        options=sorted(config.data.output_keys),
        value=config.data.output_keys[0],
        label="choose target",
    )
    dropdown
    return (dropdown,)


@app.cell
def __(config, dropdown, pl, targets):
    idx = config.data.output_keys.index(dropdown.value)
    data = targets.select(pl.col("experiment"), pl.col(dropdown.value))
    return data, idx


app._unparsable_cell(
    r"""

    norm = sns.displot(
        data=data,
        x=dropdown.value,
        hue=\"experiment\",
        kde=False,
        multiple=\"dodge\",
    )
    norm.set(ylim=(0, 15_000))
    mo.ui.
    """,
    name="__",
)


@app.cell
def __(mo, targets):
    mo.ui.data_explorer(targets.to_pandas())
    return


if __name__ == "__main__":
    app.run()
