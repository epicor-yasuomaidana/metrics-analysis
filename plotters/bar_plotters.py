from matplotlib import pyplot as plt
from matplotlib.container import BarContainer
from pandas import DataFrame
import seaborn as sns


def plot_bar(df: DataFrame, x_col: str, y_col: str, title: str, ylabel: str, grouper: str = "instance",
             errorbar: str = "sd",
             legend: bool = True,
             show_numbers: bool = True,
             ax: plt.Axes | None = None, estimator="max", fmt="%.0f"):
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

    plt.title(title)
    plt.ylabel(ylabel)
    if ax is None:
        plt.show()


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