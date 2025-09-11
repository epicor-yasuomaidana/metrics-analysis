import os

import matplotx
from matplotlib import pyplot as plt
from pandas import DataFrame
import seaborn as sns


def get_palette(df: DataFrame, grouper: str = "instance", palette: dict | None = None) -> tuple[dict, list]:
    if palette is None:
        instances = df[grouper].unique()
        palette = dict(zip(instances, sns.color_palette("tab10", len(instances))))
    else:
        instances = palette.keys()
    return palette, list(instances)


def save_plot_if_new(filename: str, dpi: int = 300, style: str = matplotx.styles.dracula, force: bool = False):
    """
    Save the current matplotlib figure to `filename` only if it does not exist.
    """
    if force and os.path.exists(filename):
        os.remove(filename)
    plt.tight_layout()
    if not os.path.exists(filename):
        if style:
            with plt.style.context(style):

                plt.savefig(filename, dpi=dpi, transparent=True)
        else:
            plt.savefig(filename, dpi=dpi, transparent=True)
        print(f"Plot saved to {filename}")
