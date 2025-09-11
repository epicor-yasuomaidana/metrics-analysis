from typing import Callable
import re
import pandas as pd
from pandas import DataFrame


def cast_string_duration_to_seconds(series: pd.Series) -> pd.Series:
    def parse_duration(value):
        if pd.isnull(value):
            return pd.NA

        total_seconds = 0.0
        matches = re.findall(r'([\d.]+)\s*(s|ms)', value)
        for amount, unit in matches:
            if unit == 's':
                total_seconds += pd.Timedelta(f'{amount}s').total_seconds()
            elif unit == 'ms':
                total_seconds += pd.Timedelta(f'{amount}ms').total_seconds()
        return total_seconds

    return series.apply(parse_duration)


def load_normalized_csv(file_path: str, time_column: str = "Time") -> DataFrame:
    df = pd.read_csv(file_path, parse_dates=[time_column])
    df.Time -= df.Time.min()
    df["dT"] = df[time_column].diff().dt.total_seconds()
    df.set_index(time_column, inplace=True)
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


def load_sum_total(file_path: str, columns_to_sum: list[str], caster=cast_string_duration_to_seconds) -> DataFrame:
    df = load_with_caster(file_path, columns_to_cast=columns_to_sum, caster=caster)
    df["total"] = df[columns_to_sum].sum(axis=1)
    return df


def load_mean_df(file_path, columns_to_average, caster=cast_string_duration_to_seconds) -> DataFrame:
    df = load_with_caster(file_path, columns_to_cast=columns_to_average, caster=caster)
    df["mean"] = df[columns_to_average].mean(axis=1)
    return df


def load_rates_per_scenario(path: str, scenarios, rate_columns: tuple[str, ...] = ("total",)) -> pd.DataFrame:
    df = load_sum_total(path, scenarios)
    for col in rate_columns:
        df[f"{col}_rate"] = df[col].diff() / df["dT"]
    return df


def get_os_and_processor(name: str) -> tuple[str, str]:
    os_ = "Windows" if "perfw" in name.lower() else "Linux"
    processor = "AMD" if "amd" in name.lower() else "Intel"
    return os_, processor


def merge_dashboards(stored_data: dict[str, dict], dashboard_name: str, loader: Callable,
                     scenarios: list[str] = None) -> pd.DataFrame:
    if scenarios is None:
        scenarios = ['BAQ', 'PartMaintenance', 'PartTracker', 'CustomerTracker',
                     'SalesOrderTracker', 'CopySalesOrder', 'POEntry20',
                     'MiscARInvoice', 'SOEntry10ShipTos', 'POEntry10', 'ProcessMRP',
                     'QuoteEntry', 'GLJournalTracker', 'QuantityOnHandCheck',
                     'SalesOrderEntry', 'ARInvoiceTracker', 'SalesOrderErrorNO',
                     'JobTracker', 'SalesOrderErrorYES']
    dfs = []
    for data in stored_data.values():
        vus = data["vus"]
        test_instance, identifier = data["instance_identifier"]
        dashboards = data["dashboards"]

        df = loader(dashboards[dashboard_name], scenarios)
        df["vus"] = vus
        df["instance"] = "{} {}".format(*get_os_and_processor(test_instance))
        df["identifier"] = identifier
        df["os"], df["processor"] = get_os_and_processor(test_instance)
        dfs.append(df)

    return pd.concat(dfs).sort_index()
