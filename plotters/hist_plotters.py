import numpy as np
from matplotlib import pyplot as plt
import matplotlib.lines as mlines
import seaborn as sns
from matplotlib.axes import Axes
from pandas import DataFrame


def plot_throughput_hist(
        x_col: str,
        df: DataFrame,
        unit: str,
        ylabel: str,
        title: str,
        ax: Axes = None,
        palette: dict = None
):
    if palette is None:
        instances = df["instance"].unique()
        palette = dict(zip(instances, sns.color_palette("tab10", len(instances))))
    else:
        instances = palette.keys()

    plt.rcParams["text.usetex"] = True

    if ax is None:
        fig, ax = plt.subplots(figsize=(9, 2.5))

    sns.histplot(df.reset_index(), x=x_col, hue="instance", kde=True, palette=palette, ax=ax, multiple="layer")

    line_handles = []
    data = {}
    for name, group in df.groupby("instance"):
        mean = group[x_col].mean()
        ax.axvline(mean, color=palette[name], linestyle="-")
        line_handles.append(mlines.Line2D([], [], color=palette[name], linestyle="-", label=rf"$\bar{{x}}$"))
        std = group[x_col].std()

        p25 = float(np.percentile(group[x_col], 25))
        p75 = float(np.percentile(group[x_col], 75))
        ax.axvline(p25, color=palette[name], linestyle=":")
        ax.axvline(p75, color=palette[name], linestyle=":")

        line_handles.append(mlines.Line2D([], [], color=palette[name], linestyle=":", label="25th/75th pct"))

        data[name] = {"mean": mean, "std": std}

    hist_handles = [
        mlines.Line2D(
            [], [], color=palette[name], marker='s', linestyle='',
            label=rf"{name} $\bar{{x}}$={data[name]['mean']:0.2f} [{unit}] $\sigma$={data[name]['std']:0.2f} [{unit}]"
        )
        for name in instances
    ]

    hist_handles.extend(line_handles)
    legend1 = ax.legend(handles=hist_handles, title="", loc="upper left")
    ax.add_artist(legend1)

    ax.set_title(title)
    ax.set_ylabel(ylabel)
    ax.set_xlabel(unit)
    if ax is None:
        plt.show()
