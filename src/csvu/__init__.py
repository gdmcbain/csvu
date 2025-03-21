from pathlib import Path

import pandas
import pint_pandas


def read_csv(filepath: Path) -> pandas.DataFrame:
    raw = pandas.read_csv(filepath)
    columns, units = zip(*raw.columns.map(lambda c: c.split("/", 1)))
    raw.columns = [c.rstrip() for c in columns]
    return raw.astype(
        dict(zip(raw.columns, [f"pint[{u.strip(' ()')}]" for u in units]))
    )


def write_csv(df: pandas.DataFrame, filepath: Path) -> None:
    def prettify_units(t) -> str:
        s = f"{t.units}"
        return f"({s})" if " " in s else s

    columns = {c: f"{c} / {prettify_units(df.dtypes[c])}" for c in df.columns}
    df.astype(float).rename(columns=columns).set_index(columns[df.columns[0]]).to_csv(
        filepath
    )
