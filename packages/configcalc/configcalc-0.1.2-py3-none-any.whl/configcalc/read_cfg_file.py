import tomllib
from collections.abc import Callable
from decimal import Decimal
from pathlib import Path
from typing import Any


def read_config_file(path: Path, parse_float: type[float] | Callable[[str], Decimal] = float) -> dict[str, Any]:
    """use parse_float argument to select whether you want numbers to be recognized
    as float or Decimal (typically)"""
    content = tomllib.load(path.open("rb"), parse_float=parse_float)
    return content
