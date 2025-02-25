from typing import Any
from functools import reduce


def merge_dict(dict1: dict[Any, Any], dict2: dict[Any, Any]) -> dict[Any, Any]:
    """from https://stackoverflow.com/a/58742155"""
    for key, val in dict1.items():
        if type(val) == dict:
            if key in dict2 and type(dict2[key] == dict):
                merge_dict(dict1[key], dict2[key])
        else:
            if key in dict2:
                dict1[key] = dict2[key]

    for key, val in dict2.items():
        if not key in dict1:
            dict1[key] = val

    return dict1


def merge_configs(*configs: dict[str, Any]) -> None:
    reduce(merge_dict, configs)
