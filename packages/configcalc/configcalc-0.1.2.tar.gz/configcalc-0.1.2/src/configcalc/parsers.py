from collections.abc import Callable
from decimal import Decimal

import pyparsing as pp

from configcalc.utils import NumberType


def decimal_parser() -> pp.ParserElement:
    """Parse numbers as Decimal

    Returns:
        pp.ParserElement: Decimal ParserElement for pyparsing
    """

    def convert_to_decimal(token: pp.ParseResults) -> Decimal:
        return Decimal(str(token[0]))

    int_part = pp.Opt(pp.one_of("- +")) + pp.Word(pp.nums)
    mantissa = int_part + pp.Opt("." + pp.Opt(pp.Word(pp.nums)))
    exponent_part = pp.Opt(
        pp.one_of("e E") + pp.Opt(pp.one_of("- +")) + pp.Word(pp.nums)
    )
    number = pp.Combine(mantissa + exponent_part)
    number.set_parse_action(convert_to_decimal)
    return number


def regular_number_parser() -> pp.ParserElement:
    """Parse numbers as default from pyparsing

    Returns:
        pp.ParserElement: Common number ParserElement for pyparsing
    """
    return pp.common.number


number_formatters = {
    NumberType.DECIMAL: (decimal_parser, Decimal),
    NumberType.FLOAT: (regular_number_parser, float),
}


def var_name_parser() -> pp.ParserElement:
    """Parse a variable number composed of a base name and a tree like structure
    using dots (.) or a list like structure using square brackets ([]), or a combination of both.

    Returns:
        pp.ParserElement: var name ParserElement for pyparsing
    """
    dict_like_key = pp.Suppress(".") + pp.common.identifier
    list_like_index = pp.Suppress("[") + pp.common.integer + pp.Suppress("]")
    subvar_element = dict_like_key ^ list_like_index
    return pp.Group(pp.common.identifier + subvar_element[...], aslist=True)


def operator_operand_expr(
    number_parser: Callable[[], pp.ParserElement],
) -> pp.ParserElement:
    """Parse an operator operand with priority. In order (most priority to least) the minus sign (-), exponent (^), multiply/divide (* /) and add/substract (+ -)

    Args:
        number_parser (Callable[[], pp.ParserElement]): number parser like decimal_parser or regular_number_parser

    Returns:
        pp.ParserElement: operand parser for pyparsing
    """
    operator_operand = pp.Forward()
    number = number_parser()
    var_name = var_name_parser()
    function_struct = (
        pp.common.identifier + pp.Suppress("(") + operator_operand + pp.Suppress(")")
    )

    operand = function_struct | number | var_name
    operator_operand <<= pp.infix_notation(
        operand,
        [
            ("-", 1, pp.OpAssoc.RIGHT),
            ("^", 2, pp.OpAssoc.LEFT),
            (pp.one_of("* /"), 2, pp.OpAssoc.LEFT),
            (pp.one_of("+ -"), 2, pp.OpAssoc.LEFT),
        ],
    )
    return operator_operand


def build_operand_parser(
    number_parser: Callable[[], pp.ParserElement],
) -> pp.ParserElement:
    """Builds the operand parser by removing the = sign at the beginning of the formula

    Args:
        number_parser (Callable[[], pp.ParserElement]): number parser like decimal_parser or regular_number_parser

    Returns:
        pp.ParserElement: full formula parser for pyparsing
    """
    operator_operand = operator_operand_expr(number_parser)
    return pp.Suppress("=") + operator_operand
