from pandas import DataFrame
import seaborn as sns


def get_palette(df: DataFrame, grouper: str = "instance", palette: dict | None = None) -> tuple[dict, list]:
    if palette is None:
        instances = df[grouper].unique()
        palette = dict(zip(instances, sns.color_palette("tab10", len(instances))))
    else:
        instances = palette.keys()
    return palette, list(instances)
