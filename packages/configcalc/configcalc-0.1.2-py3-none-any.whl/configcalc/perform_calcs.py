import functools
import math
from collections.abc import Callable
from decimal import Decimal
from pathlib import Path
from typing import Any

import pyparsing as pp

from configcalc.parsers import (
    number_formatters,
    build_operand_parser,
)
from configcalc.read_cfg_file import read_config_file
from configcalc.utils import (
    Number,
    NumberType,
    MATH_FUNCTIONS,
    OPERATIONS,
    get_deep,
    set_deep,
)


def find_formulas(dictionary: dict[str, Any]) -> dict[tuple[str, ...], str]:
    """finds all formulas in a nested dictionary

    Args:
        dictionary (dict[str, Any]): config dictionary

    Returns:
        dict[tuple[str, ...], str]: dictionary of formulas. Keys are a tuple of keys to access the value in the tree
    """
    formulas = {}
    for key, value in dictionary.items():
        if isinstance(value, str) and value.startswith("="):
            formulas[(key,)] = value
        elif isinstance(value, dict):
            nested_dict = find_formulas(value)
            for nested_key, nested_value in nested_dict.items():
                formulas[(key, *nested_key)] = nested_value
    return formulas


def find_var_ref_indices(parsed_lists: list[Any]) -> list[list[int]]:
    """find positions of var values in parsed formulas from the parser as a list of indices of all variables

    Args:
        parsed_lists (list[Any]): parsed formula

    Returns:
        list[list[int]]: _description_
    """
    """find positions as a list of indices of all variables in parsed lists from the parser"""
    base_elements_indices = []
    for i, element in enumerate(parsed_lists):
        # we have a var name
        if (
            isinstance(element, list)
            and isinstance(element[0], str)
            and element[0] not in MATH_FUNCTIONS
        ):
            # base_element = element[0]
            # print(element)
            base_elements_indices.append([i])
        elif isinstance(element, list):
            base_elements_indices.extend(
                [[i, *inner_indices] for inner_indices in find_var_ref_indices(element)]
            )
    return base_elements_indices


def build_ref_levels(ref_position: list[str | int]) -> list[list[str | int]]:
    ref_levels = []
    for i in reversed(range(len(ref_position))):
        ref_levels.append(ref_position[0:i])
    return ref_levels


def get_value_in_data(data: dict[str, Any], list_identifier: list[str | int]) -> Any:
    """get the value of a variable from its list identifier"""
    item = data
    for i_or_key in list_identifier:
        item = item[i_or_key]
    return item


def get_value_from_ref_list(
    data: dict[str, Any],
    list_identifier: list[str | int],
    ref_levels: list[list[str | int]],
) -> Any:
    return_value = None
    for ref_level in ref_levels:
        try:
            return_value = get_value_in_data(
                data=data, list_identifier=ref_level + list_identifier
            )
        except (KeyError, TypeError):
            continue
    return return_value


def find_inner_lists(parsed_lists: list[Any]) -> list[list[int] | None]:
    inner_lists_positions: list[list[int]] = []

    def inner_list_seeker(
        search_list: list[Any], position: list[int]
    ) -> list[int] | None:
        found_list = False
        for i, element in enumerate(search_list):
            if isinstance(element, list):
                inner_lists_positions.append(inner_list_seeker(element, [*position, i]))
                found_list = True
        if not found_list:
            return position

    inner_list_seeker(parsed_lists, position=[])
    return [position for position in inner_lists_positions if position is not None]


def calc_result_update(
    result: Number | None, value: Number, operation: str | None = None
) -> Number:
    if result is None or operation is None:
        return value
    else:
        return OPERATIONS[operation](result, value)


def calc_math_func_result(function_name: "str", function_arg: Number):
    return getattr(math, function_name)(function_arg)


def calculate_local(
    calc_list: list[Number | str], parse_float: type[float] | Callable[[str], Decimal]
) -> Number:
    result = 0
    operator = "+"
    i = 0
    while i < len(calc_list):
        operand_or_operator = calc_list[i]
        if operand_or_operator in list(OPERATIONS.keys()):
            operator = operand_or_operator
        else:
            if operand_or_operator in MATH_FUNCTIONS:
                operand = parse_float(
                    calc_math_func_result(
                        function_name=operand_or_operator, function_arg=calc_list[i + 1]
                    )
                )
                i += 1
            else:
                operand = operand_or_operator
            result = calc_result_update(result, operand, operator)
        i += 1

    return result


def calculate_formula_w_value(
    parsed_formula_w_value: list[Any],
    parse_float: type[float] | Callable[[str], Decimal],
) -> Number:
    inner_lists = find_inner_lists(parsed_formula_w_value)

    while len(inner_lists) > 0:
        for inner_list in inner_lists:
            calc_list = get_deep(parsed_formula_w_value, inner_list)
            local_result = calculate_local(calc_list=calc_list, parse_float=parse_float)
            set_deep(parsed_formula_w_value, inner_list, local_result)
        inner_lists = find_inner_lists(parsed_formula_w_value)

    return parsed_formula_w_value[0]


def _parse_any_value(
    value: str | Number, operand_parser: pp.ParserElement
) -> list[Any] | Any:
    if isinstance(value, str) and value.startswith("="):
        parsed_new_val = operand_parser.parse_string(value).asList()
    else:
        parsed_new_val = value
    return parsed_new_val


def replace_vars_by_values(
    parsed_formula: list[Number | str],
    data: dict[str, Any],
    formula_position: list[int],
    context_variables: dict[str, float | int | Decimal],
    parse_any_value: Callable[[str | Number], Number],
) -> list[Number | str]:
    while True:
        var_ref_indices = find_var_ref_indices(parsed_formula)
        if var_ref_indices == []:
            break
        for var_ref_index in var_ref_indices:
            var_ref = get_deep(parsed_formula, var_ref_index)
            try:
                parsed_new_val = context_variables[var_ref[0]]
            except (KeyError, TypeError):
                ref_levels = build_ref_levels(formula_position)
                var_new_val = get_value_from_ref_list(
                    data, list_identifier=var_ref, ref_levels=ref_levels
                )
                parsed_new_val = parse_any_value(var_new_val)
            set_deep(parsed_formula, var_ref_index, parsed_new_val)

    return parsed_formula


def perform_calculations(
    config: dict[str, Any],
    context_variables: dict[str, Any] | None = None,
    number_type: NumberType = NumberType.FLOAT,
) -> dict[str, Any]:
    """resolves all possible calculations in config dictionary

    Args:
        config (dict[str, Any]): config dictionary as given by read_config_file
        context_variables (dict[str, Any] | None, optional): additional variable values to use for calculations. Defaults to None.
        number_type (NumberType, optional): number type to use (e.g. NumberType.DECIMAL). Defaults to FLOAT.

    Returns:
        dict[str, Any]: config dictionary with all calculations resolved
    """

    if context_variables is None:
        context_variables = {}
    number_parser_element, number_parser_function = number_formatters[number_type]
    operand_parser = build_operand_parser(number_parser=number_parser_element)
    parse_any_value = functools.partial(_parse_any_value, operand_parser=operand_parser)
    formulas = find_formulas(config)
    for formula_position, formula in list(formulas.items()):
        parsed_formula = operand_parser.parse_string(formula).asList()
        parsed_formula_w_value = replace_vars_by_values(
            parsed_formula=parsed_formula,
            data=config,
            formula_position=list(formula_position),
            context_variables=context_variables,
            parse_any_value=parse_any_value,
        )
        calculated_value = calculate_formula_w_value(
            parsed_formula_w_value, parse_float=number_parser_function
        )
        set_deep(
            nested_list=config, indices=list(formula_position), value=calculated_value
        )
    return config


if __name__ == "__main__":
    config = read_config_file(Path(r"tests/assets/test.toml"), parse_float=Decimal)

    print(
        perform_calculations(
            config=config,
            context_variables={"_input_parts": 25},
            number_formatter=number_formatters["decimal"],
        )
    )
