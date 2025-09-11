from pandas import DataFrame


def summarize_by_grouper(df: DataFrame, to_process: list[str], summarizer: str = "max", grouper: str = "instance"):
    return df[[grouper] + to_process].groupby(grouper).agg(summarizer).reset_index()
