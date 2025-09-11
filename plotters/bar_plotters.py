import os

import matplotx
from matplotlib import pyplot as plt
from matplotlib.container import BarContainer
from numpy import ceil
from pandas import DataFrame
from typing import Literal, Iterable
import seaborn as sns


def plot_bar(df: DataFrame, x_col: str, y_col: str, title: str, ylabel: str, grouper: str = "instance",
             errorbar: str | tuple[str, float] | Iterable[float] | None = "sd",
             legend: bool = True,
             show_numbers: bool = True,
             ax: plt.Axes | None = None, estimator="max", fmt="%.0f",
             ticks_params: tuple[Literal["both", "x", "y"], dict] = ()):
    instances = df[grouper].unique()
    palette = dict(zip(instances, sns.color_palette("tab10", len(instances))))

    if ax is None:
        fig, ax = plt.subplots(figsize=(7.5, 5))

    sns.barplot(
        data=df.reset_index(),
        x=x_col, y=y_col, hue=grouper,
        ax=ax, palette=palette, errorbar=errorbar, legend=legend, estimator=estimator
    )
    if show_numbers:
        for container in ax.containers:
            if isinstance(container, BarContainer):
                ax.bar_label(container, fmt=fmt)
    for axis, params in ticks_params:
        ax.tick_params(axis=axis, **params)

    plt.title(title)
    plt.ylabel(ylabel)
    if ax is None:
        plt.show()


def plot_bars(df: DataFrame, to_plot: list[str] = None, summarizer: str = "max", grouper: str = "instance",
              ax: plt.Axes | None = None, title: str = "", ylabel: str = "", formatter: str = "%.0f",
              bar_label_rotation_padding: tuple[int, int] = (45, 3),
              axis_params: tuple[str, dict] = ("x", {"rotation": 45})):
    if ax is None:
        fig, ax = plt.subplots(figsize=(22, 5))

    processing = df[[grouper] + to_plot].groupby(grouper).agg(summarizer).reset_index()
    melted = processing.melt(id_vars=grouper, value_vars=tuple(to_plot), var_name="scenario", value_name="value")
    ax = sns.barplot(data=melted, x="scenario", y="value", hue=grouper, ax=ax)
    for container in ax.containers:
        if isinstance(container, BarContainer):
            ax.bar_label(container, fmt=formatter, rotation=bar_label_rotation_padding[0],
                         padding=bar_label_rotation_padding[1])
    for axis, params in (axis_params,):
        ax.tick_params(axis='x', **params)

    ax.set_title(title)
    ax.set_ylabel(ylabel)


def plot_cat_bar(
        df: DataFrame,
        y_col: str,
        axis_labels: tuple[str, str],
        title: str,
        x_col: str = "processor",
        hue_col: str = "os",
        row_col: str = "vus",
        errorbar: str = "sd",
        palette: dict = None,
):
    instances = df[hue_col].unique()
    if palette is None:
        palette = dict(zip(instances, sns.color_palette("tab10", len(instances))))
    g = sns.catplot(
        data=df.reset_index(), kind="bar",
        x=x_col, y=y_col, hue=hue_col, row=row_col,
        errorbar=errorbar, palette=palette
    )
    g.despine(left=True)
    g.set_axis_labels(*axis_labels)
    plt.title(title)
    plt.show()
    return g


def plot_bars_chunked(df: DataFrame, to_process, chunk_size=5, grouper: str = "instance", output_dir: str = "plots",
                      title: str = "", ylabel: str = "", dpi: int = 300,
                      style: str = matplotx.styles.dracula, force: bool = False):
    import math
    from plotters.common import save_plot_if_new
    os.makedirs(output_dir, exist_ok=True)
    n_chunks = math.ceil(len(to_process) / chunk_size)
    for i in range(n_chunks):
        chunk = to_process[i * chunk_size:(i + 1) * chunk_size]
        fig, ax = plt.subplots(figsize=(10, 5))
        processing = df[[grouper] + chunk].groupby(grouper).max().reset_index()
        melted = processing.melt(id_vars=grouper, value_vars=chunk, var_name="scenario", value_name="value")
        sns.barplot(data=melted, x="scenario", y="value", hue=grouper, ax=ax)
        for container in ax.containers:
            ax.bar_label(container, fmt="%.0f", rotation=45, padding=3)
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel(ylabel)
        plt.tight_layout()
        filename = os.path.join(output_dir, f"{title.replace(' ', '_')}_chunk_{i + 1}.png")
        save_plot_if_new(filename, dpi=dpi, style=style, force=force)
        plt.close(fig)
