from collections.abc import Callable
from functools import partial
from pathlib import Path
from typing import Tuple, Union

import pandas as pd
import pint
import pint_pandas


def parse_algebraic(name: str, delimiter: str = "/") -> Tuple[str, str]:
    quantity = name.split(delimiter, 1)
    return quantity[0].rstrip(), (
        quantity[1].strip(" ()") if quantity[1:] else "dimensionless"
    )


def parse_bracketed(name: str, brackets: str = "()") -> Tuple[str, str]:
    quantity = name.split(brackets[0], 1)
    return quantity[0].rstrip(), (
        quantity[1].rstrip(f"{brackets[1]} ") if quantity[1:] else "dimensionless"
    )


def read_csv(
    filepath: Path,
    parse: Union[Callable[[str], Tuple[str, str]], str] = "()",
) -> pd.DataFrame:
    df = pd.read_csv(filepath)

    if parse in ["()", "[]", "{}", "<>", "APS"]:
        parse = partial(parse_bracketed, brackets=parse)
    elif parse in ["/", ",", ":", "IUPAC"]:
        parse = partial(parse_algebraic, delimiter=parse)

    df.columns = pd.MultiIndex.from_tuples(df.columns.map(parse))

    pint.get_application_registry()
    return df.pint.quantify()


def write_bracketed(name: str, unit: pint.Unit, delimiter: str = "()") -> str:
    return f"{name} {delimiter[0]}{unit}{delimiter[1]}"


def write_formatted(name: str, unit: pint.Unit, fmt: str = "{} ({})") -> str:
    return fmt.format(name, unit)


def write_algebraic(name: str, unit: pint.Unit, operator: str = "/") -> str:
    u = f"{unit}"
    return f"{name} {operator} ({u})" if "/" in u else f"{name} {operator} {unit}"


def write_csv(
    df: pd.DataFrame,
    filepath: Path,
    fmt: Union[Callable[[str, pint.Unit], str], str] = write_bracketed,
) -> None:
    if isinstance(fmt, str):
        fmt = fmt.format
    columns = {c: fmt(c, df.dtypes[c].units) for c in df.columns}
    df.astype(float).rename(columns=columns).set_index(columns[df.columns[0]]).to_csv(
        filepath
    )
