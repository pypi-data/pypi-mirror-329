
from config import paths, data, experiment as exp_conf
import seaborn as sns
import matplotlib.pyplot as plt
import click
import numpy as np
import pandas as pd
from emulator.inference import data_from_weights
from sklearn.metrics import r2_score
from tqdm import tqdm
from itertools import product
import logging


@click.group()
def cli():
    """plot r2 results"""


@cli.command("sweep")
def sweep():
    """plot r2 vs. training size from previously generated data"""
    load_from = paths.data() / "training_size_sweep_r2.csv"
    df = pd.read_csv(load_from, sep="|")
    df.set_index(["region", "year", "feature", "scenarios"], inplace=True)
    plt.style.use("ggplot")  # makes plot looks much nicer
    fig = plt.figure(figsize=(15, 4))
    ax = fig.subplots(1, 3, sharey=True)
    for i, group in enumerate(["region", "year", "feature"]):
        sns.lineplot(
            df.groupby(["scenarios", group]).median(),
            x="scenarios",
            y="r2",
            hue=group,
            ax=ax[i],
            palette="tab10",
        )
        ax[i].set_ylim(0, 1)
        ax[i].set_title(f"{group}s")
        ax[i].legend().remove()
    plt.tight_layout()
    save_to = paths.docs() / "figures" / "r2_versus_scenarios.png"
    plt.savefig(save_to, dpi=300, bbox_inches="tight")
    logging.info(f"saved: {save_to}")


@cli.command("cartesian")
def cartesian():
    """plot the cartesian product of training x dev sets"""
    parent = paths.data() / "cartesian"
    pairs = [
        (x, y) for x, y in product(exp_conf.train_sources(), exp_conf.dev_sources())
    ]

    dfs = []
    for train, dev in pairs:
        file = f"r2_score_train:{train}_dev:{dev}.csv"
        df = pd.read_csv(parent / file, sep="|")
        dfs.append(df)
    df = pd.concat(dfs)

    collect = []
    out = df.groupby(["train"])["r2"].median().groupby(["train"]).mean()
    out.name = "overall"
    collect.append(out)
    for metric in ["region", "year", "feature"]:
        out = df.groupby(["train", metric])[
            "r2"].median().groupby(["train"]).mean()
        out.name = metric
        collect.append(out)
    result = pd.concat(collect, axis=1)                                                                                                                                                print(result)

    collect = []
    out = (                                                                                                                                                                                df[df.train == df.dev]
        .groupby(["train"])["r2"]
        .median()
        .groupby(["train"])
        .mean()
    )
    out.name = "overall"
    collect.append(out)
    for metric in ["region", "year", "feature"]:
        out = (
            df[df.train == df.dev]
            .groupby(["train", metric])["r2"]
            .median()
            .groupby(["train"])
            .mean()
        )
        out.name = metric
        collect.append(out)
        result = pd.concat(collect, axis=1)
        print(result)



                                                                                                                                                                                   @cli.command()
@click.option("-t", "--train_source", default="interp_sobol")
@click.option("-d", "--dev_source", default="interp_sobol")
@click.option(
    "-w",
    "--weights",
    default="years_baseline_debug_mixed_train:dawn_exp1_jr_dev:dawn_exp1_jr_depth:4_2023_10_11",
)
                                                                                                                                                                                   def pitfall(train_source, dev_source, weights):
    """plot an example of why we use r2 on a per feature basis"""
    gen_df, val_df, _ = data_from_weights(train_source, dev_source, weights)
    feature = "energy_demand_elec_transport"
    plt.style.use("ggplot")  # makes plot looks much nicer

    pred_y = gen_df.xs(2050, level="year")[feature]
    true_y = val_df.xs(2050, level="year")[feature]
    _, ax = plt.subplots(1, 2, sharey=True)
    r2 = r2_score(true_y, pred_y)
    one = np.linspace(true_y.min(), true_y.max(), 100)
    sns.scatterplot(x=pred_y, y=true_y, hue=true_y.index.values, ax=ax[0])
    sns.lineplot(x=one, y=one, color="red", ax=ax[0])
    ax[0].text(0.1, 0.8, f"r2 score: {r2:.2f}", transform=ax[0].transAxes)
    ax[0].get_legend().set_visible(False)
    ax[0].set_title(f"{feature}\nacross regions")
    ax[0].set_xlabel("emulator")
    ax[0].set_ylabel("core")
    ax[0].set_box_aspect(1)

    pred_y = gen_df.loc[["China"]].xs(2050, level="year")[feature]
    true_y = val_df.loc[["China"]].xs(2050, level="year")[feature]
    r2 = r2_score(true_y, pred_y)
    sns.scatterplot(x=pred_y, y=true_y, hue=true_y.index.values, ax=ax[1])
    sns.lineplot(x=one, y=one, color="red", ax=ax[1])
    ax[1].text(0.1, 0.8, f"r2 score: {r2:.2f}", transform=ax[1].transAxes)
    ax[1].set_title(f"{feature}\nChina only")
    ax[1].set_xlabel("emulator")
    ax[1].set_box_aspect(1)

    save_to = paths.docs() / "figures" / "r2_why_we_group.png"
    plt.savefig(save_to, dpi=300)
    logging.info(f"saved: {save_to}")
    plt.close()


                                                                                                                                                                                                                                                                                                                                                                      @cli.command()
@click.option("-t", "--train_source", default="interp_sobol")
@click.option("-d", "--dev_source", default="interp_sobol")
@click.option(
    "-w",
    "--weights",
    default="years_baseline_debug_mixed_train:dawn_exp1_jr_dev:dawn_exp1_jr_depth:4_2023_10_11",
)
def entire_dataset(train_source, dev_source, weights):
    """plot r2 vs the core across all data"""
    plt.style.use("ggplot")  # makes plot looks much nicer
    pred_y, true_y = data_from_weights(train_source, dev_source, weights)
    r2 = r2_score(true_y, pred_y)
    one = np.linspace(true_y.values.min(), true_y.values.max(), 100)
    ax = sns.scatterplot(x=pred_y.values.flatten(), y=true_y.values.flatten())
    sns.lineplot(x=one, y=one, color="red")
    ax.text(true_y.values.mean(), 45, f"r2 score: {r2:.2f}")
    ax.set_xlabel("emulator")
    ax.set_ylabel("core")
    ax.set_xlim(0, 10_000)
    ax.set_ylim(0, 10_000)

    save_to = paths.docs() / "figures" / "r2_over_all_values.png"
    plt.savefig(save_to, dpi=300)
    logging.info(f"saved: {save_to}")
    plt.close()
