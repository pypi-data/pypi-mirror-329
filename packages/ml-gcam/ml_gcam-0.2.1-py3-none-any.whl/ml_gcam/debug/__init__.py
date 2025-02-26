import matplotlib.pyplot as plt
import polars as pl
import seaborn as sns
from matplotlib.figure import Figure


def plot_dimensions_with_negative_scores(scores: pl.DataFrame) -> Figure:
    fig, ax = plt.subplots(3, 1)
    sns.histplot(scores, hue="region", x="r2", ax=ax[0], cbar="tab20", legend=None)
    sns.histplot(scores, hue="year", x="r2", ax=ax[1], cbar="tab20", legend=None)
    sns.histplot(scores, hue="output", x="r2", ax=ax[2], cbar="tab20", legend=None)
    fig.tight_layout()
    plt.close()
    return fig


def debug_nuclear(dataset):
    from ..config import config
    from tqdm import tqdm
    from sklearn.metrics import r2_score
    from itertools import product
    import numpy as np
    
    inputs = ["back", "bio", "ccs", "elec", "emiss", "energy", "ff", "solarS", "solarT", "windS", "windT",]
    combinations = dataset.select(inputs).unique()
    
    collect_mse = []
    collect_r2 = []
    for combo in tqdm(combinations.iter_rows(named=True)):
        scenarios = dataset.filter(
                (pl.col("back") == combo["back"]),
                (pl.col("bio") == combo["bio"]),
                (pl.col("ccs") == combo["ccs"]),
                (pl.col("elec") == combo["elec"]),
                (pl.col("emiss") == combo["emiss"]),
                (pl.col("energy") == combo["energy"]),
                (pl.col("ff") == combo["ff"]),
                (pl.col("solarS") == combo["solarS"]),
                (pl.col("solarT") == combo["solarT"]),
                (pl.col("windS") == combo["windS"]),
                (pl.col("windT") == combo["windT"]))

        nuc_values = scenarios['nuc'].unique()
        if len(nuc_values) <= 1:
            continue

        nuc_hi = scenarios.filter((pl.col("nuc") == nuc_values[0]))
        nuc_lo = scenarios.filter((pl.col("nuc") == nuc_values[1]))

        if len(nuc_hi) == 0 or len(nuc_lo) == 0:
            continue

        hi_values = nuc_hi[config.data.output_keys].to_pandas().values.flatten()
        lo_values = nuc_lo[config.data.output_keys].to_pandas().values.flatten()

        mse = np.linalg.norm(hi_values - lo_values)
        r2 = r2_score(hi_values, lo_values)

        collect_mse.append(mse)
        collect_r2.append(r2)

    breakpoint()
