import pandas as pd
from pandas import DataFrame


def cast_string_duration_to_seconds(series: pd.Series) -> pd.Series:
    def parse_duration(value):
        if pd.isnull(value):
            return pd.NA

        import re
        total_seconds = 0.0
        matches = re.findall(r'([\d.]+)\s*(s|ms)', value)
        for amount, unit in matches:
            if unit == 's':
                total_seconds += pd.Timedelta(f'{amount}s').total_seconds()
            elif unit == 'ms':
                total_seconds += pd.Timedelta(f'{amount}ms').total_seconds()
        return total_seconds

    return series.apply(parse_duration)


def load_normalized_csv(file_path: str) -> DataFrame:
    df = pd.read_csv(file_path, parse_dates=['Time'])
    df.Time -= df.Time.min()
    df["dT"] = df["Time"].diff().dt.total_seconds()
    df.set_index('Time', inplace=True)
    df.sort_index(inplace=True)
    return df


def load_with_caster(file_path, columns_to_cast=None, caster=cast_string_duration_to_seconds) -> DataFrame:
    df = load_normalized_csv(file_path)
    if columns_to_cast is None:
        columns_to_cast = [col for col in df.columns if col != "dT"]
    if not all(pd.api.types.is_numeric_dtype(df[col]) for col in columns_to_cast):
        for col in columns_to_cast:
            df[col] = caster(df[col])
    return df




def load_sum_total(file_path, columns_to_sum, caster=cast_string_duration_to_seconds) -> DataFrame:
    df = load_with_caster(file_path, columns_to_cast=columns_to_sum, caster=caster)
    df["total"] = df[columns_to_sum].sum(axis=1)
    return df

def load_mean_df(file_path, columns_to_average, caster=cast_string_duration_to_seconds) -> DataFrame:
    df = load_with_caster(file_path, columns_to_cast=columns_to_average, caster=caster)
    df["mean"] = df[columns_to_average].mean(axis=1)
    return df


if __name__ == '__main__':
    # file_path_ = "../quick/perflamd1_2025-08-22_12-50-00-Avg Iteration Duration p99.csv"
    # normalized_df = load_normalized_csv(file_path_)
    # print(normalized_df.head())
    file_path_ ="../quick/perflamd1_2025-08-22_12-50-00-TTFB per Scenario.csv"
    sum_total_df = load_sum_total(file_path_)
    print(sum_total_df.head())
