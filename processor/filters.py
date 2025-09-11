import pandas as pd

import re

def parse_time_str(s):
    if not isinstance(s, str):
        return s
    h = m = 0
    match = re.match(r'(?:(\d+)h)?\s*(?:(\d+)m)?', s)
    if match:
        h = int(match.group(1) or 0)
        m = int(match.group(2) or 0)
    return pd.Timedelta(hours=h, minutes=m)

def cut_by_range(df, start_time_str, end_time_str):
    start_time = parse_time_str(start_time_str)
    end_time = parse_time_str(end_time_str)
    return df[(df.index >= start_time) & (df.index <= end_time)]

def relative_cut_by_range(df, start_offset_str, end_offset_str):
    start_offset = parse_time_str(start_offset_str)
    end_offset = parse_time_str(end_offset_str)
    start_time = df.index.min() + start_offset
    end_time = df.index.min() + end_offset
    return df[(df.index >= start_time) & (df.index <= end_time)]

def cut_by_window(df, start_time_str, duration):
    start_time = parse_time_str(start_time_str)
    end_time = start_time + parse_time_str(duration)
    return cut_by_range(df, start_time, end_time)

def filter_wrong_totals(df: pd.DataFrame, total_column="total", grouper_column="instance") -> pd.DataFrame:
    result = []
    for _, column_group in df.groupby(grouper_column):
        filtered = column_group[column_group[total_column].diff() >= 0]
        result.append(filtered)
    return pd.concat(result)