"""Contains all the necessary parsers for discord messages"""
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, \
    implicit_multiplication_application, convert_xor


def to_sympy(message):
    """
    Parses a string containing mathematical expressions into sympy syntax.

    Args:
        message(str): A discord text message containing a mathematical
            expression.

    Returns:
        sympy: The parsed expression.

    """
    transformations = (standard_transformations +
                       (implicit_multiplication_application, convert_xor))
    return parse_expr(message, transformations=transformations)
