from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns

from ..table import fraction_binary_vs_r2
from ..data import experiment_name_to_paper_label


def plot_fraction_binary(score_path: Path, aggregation: str):
    scores = fraction_binary_vs_r2(score_path, aggregation).to_pandas()
    scores['dev_source'] = scores['dev_source'].map(experiment_name_to_paper_label)
    fig, ax = plt.subplots()
    sns.lineplot(scores, x="fraction_binary", y=f"r2_{aggregation}", hue="dev_source", ax=ax)
    plt.ylim([0,1.01])
    plt.close()
    fig.tight_layout()

    return fig
