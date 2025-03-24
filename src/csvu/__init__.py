from pathlib import Path
from typing import Callable, Tuple

import pandas as pd
import pint_pandas


def parse_raw_name(name: str) -> Tuple[str, str]:
    quantity = name.split("/", 1)
    return quantity[0], (quantity[1].strip(" ()") if quantity[1:] else "dimensionless")


def read_csv(
    filepath: Path, parse_raw_name: Callable[[str], Tuple[str, str]] = parse_raw_name
) -> pd.DataFrame:
    df = pd.read_csv(filepath)
    df.columns = pd.MultiIndex.from_tuples([parse_raw_name(c) for c in df.columns])
    return df.pint.quantify()


def write_csv(df: pd.DataFrame, filepath: Path) -> None:
    def prettify_units(t) -> str:
        s = f"{t.units}"
        return f"({s})" if " " in s else s

    columns = {c: f"{c} / {prettify_units(df.dtypes[c])}" for c in df.columns}
    df.astype(float).rename(columns=columns).set_index(columns[df.columns[0]]).to_csv(
        filepath
    )
