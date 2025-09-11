import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from matplotlib.pyplot import subplots
from pandas import DataFrame

from plotters.common import get_palette


def plot_over_time(df: DataFrame, y_col: str, title: str, ylabel: str, grouper: str = "instance",
                   ax: Axes = None, palette: dict = None):
    palette, _ = get_palette(df, grouper, palette)

    if ax is None:
        fig, ax = subplots(figsize=(7.5, 5))
    for name, group in df.groupby(grouper):
        color = palette.get(name)
        group.plot(use_index=True, y=y_col, label=name, ax=ax, color=color)
    plt.title(title)
    plt.ylabel(ylabel)
    if ax is None:
        plt.show()


def plot_grouped_means_with_palette(
        df: DataFrame,
        value_col: str,
        ax: plt.Axes,
        group_col: str = "instance",
        palette_name: str = "tab10",
        line_style: str = "--",
        label_fmt: str = r"$\bar{{x}}$={mean:.2f}s $\sigma$={std:.2f}s"
):
    instances = df[group_col].unique()
    palette = dict(zip(instances, sns.color_palette(palette_name, len(instances))))
    for name, group in df.groupby(group_col):
        mean_value = group[value_col].mean()
        std_value = group[value_col].std()
        ax.axhline(
            mean_value,
            color=palette[name],
            linestyle=line_style,
            label=label_fmt.format(mean=mean_value, std=std_value)
        )
