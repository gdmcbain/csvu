from pathlib import Path

import pandas
import pint_pandas


def read_csv(filepath: Path) -> pandas.DataFrame:
    raw = pandas.read_csv(filepath)
    units = {}
    for c in raw:
        if "/" in c:
            column, unit = c.split("/", 1)
        else:
            column = c
            unit = "dimensionless"
        units[column.rstrip()] = f"pint[{unit.strip(' ()')}]"
    raw.columns = list(units.keys())
    return raw.astype(units)


def write_csv(df: pandas.DataFrame, filepath: Path) -> None:
    def prettify_units(t) -> str:
        s = f"{t.units}"
        return f"({s})" if " " in s else s

    columns = {c: f"{c} / {prettify_units(df.dtypes[c])}" for c in df.columns}
    df.astype(float).rename(columns=columns).set_index(columns[df.columns[0]]).to_csv(
        filepath
    )
