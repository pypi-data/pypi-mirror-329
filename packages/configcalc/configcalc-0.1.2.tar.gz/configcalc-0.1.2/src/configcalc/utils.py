from decimal import Decimal

from enum import Enum, auto
from typing import Any

import math
from collections.abc import Callable


Number = int | float | Decimal


class NumberType(Enum):
    """Enumeration FLOAT or DECIMAL to specify number type."""

    FLOAT = auto()
    DECIMAL = auto()


def get_deep(nested_list: list[Any], indices: list[int]) -> Any:
    """Gets element in nested list

    Args:
        nested_list (list[Any]): list with possible sublists
        indices (list[int]): list of indices on each list to locate the element, from top to bottom

    Returns:
        Any: element value
    """
    # see https://stackoverflow.com/a/44579249/10926757
    if (len(indices) > 1) and (isinstance(nested_list[indices[0]], (list, dict))):
        return get_deep(nested_list[indices[0]], indices[1:])
    else:
        return nested_list[indices[0]]


def set_deep(nested_list: list[Any], indices: list[int], value: Any) -> list[Any]:
    """Sets an element value deep in a nested list

    Args:
        nested_list (list[Any]): nested list
        indices (list[int]): list of indices to the element
        value (Any): new value of element

    Returns:
        list[Any]: nested list with updated value of element
    """
    if (len(indices) > 1) and isinstance(nested_list[indices[0]], (list, dict)):
        set_deep(nested_list[indices[0]], indices[1:], value)
    else:
        nested_list[indices[0]] = value
    return nested_list


OPERATIONS: dict[str, Callable[[Number, Number], Number]] = {
    r"+": lambda a, b: a + b,
    r"-": lambda a, b: a - b,
    r"*": lambda a, b: a * b,
    r"/": lambda a, b: a / b,
    r"^": lambda a, b: a**b,
}

MATH_FUNCTIONS: list[str] = []
MATH_CONSTANTS: list[str] = []
for math_object_name in dir(math):
    math_object = getattr(math, math_object_name)
    if callable(math_object) and not math_object_name.startswith("__"):
        MATH_FUNCTIONS.append(math_object_name)
    elif isinstance(math_object, float):
        MATH_CONSTANTS.append(math_object_name)
