from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Tuple, Union

import pandas as pd
import pint_pandas


def parse_raw_name_algebraic(name: str, delimiter: str = "/") -> Tuple[str, str]:
    quantity = name.split(delimiter, 1)
    return quantity[0].rstrip(), (
        quantity[1].strip(" ()") if quantity[1:] else "dimensionless"
    )


def parse_raw_name_bracketed(name: str, brackets: str = "()") -> Tuple[str, str]:
    quantity = name.split(brackets[0], 1)
    return quantity[0].rstrip(), (
        quantity[1].rstrip(f"{brackets[1]} ") if quantity[1:] else "dimensionless"
    )


def read_csv(
    filepath: Path,
    parse_raw_name: Union[Callable[[str], Tuple[str, str]], str] = "()",
) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    if parse_raw_name in ["()", "[]", "{}", "<>"]:
        parse_raw_name = partial(parse_raw_name_bracketed, brackets=parse_raw_name)
    elif parse_raw_name in ["/", ",", ":"]:
        parse_raw_name = partial(parse_raw_name_algebraic, delimiter=parse_raw_name)

    df.columns = pd.MultiIndex.from_tuples(df.columns.map(parse_raw_name))
    return df.pint.quantify()


def write_csv(df: pd.DataFrame, filepath: Path, fmt: str = "{} ({})") -> None:
    columns = {c: fmt.format(c, df.dtypes[c].units) for c in df.columns}
    df.astype(float).rename(columns=columns).set_index(columns[df.columns[0]]).to_csv(
        filepath
    )
