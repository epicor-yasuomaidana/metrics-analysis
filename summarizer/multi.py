from pandas import DataFrame, Series


def get_percentage_diff_multi(df: DataFrame, value_col: tuple, reference_instance: str) -> tuple[DataFrame, DataFrame]:
    value = df[value_col]
    reference_value = value[reference_instance]
    diff = value - reference_value
    percentage_diff = (diff / reference_value) * 100
    return diff.reset_index().set_index("instance"), percentage_diff.reset_index().set_index("instance")


def get_percentage_interpretation_multi(dest: tuple[DataFrame, DataFrame], process_col: tuple, interpreter=lambda
        x: f'{x:.2f}% faster' if x < 0 else f'{x:.2f}% slower' if x > 0 else 'same', col_name="diff (s)"):
    diff_col = dest[0][process_col]
    pct_col = dest[1][process_col]
    interpretation = pct_col.apply(interpreter)
    return DataFrame({'% diff': interpretation, col_name: diff_col})