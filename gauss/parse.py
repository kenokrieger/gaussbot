"""Contains all the necessary parsers for discord messages"""
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, \
    implicit_multiplication_application, convert_xor, split_symbols
from sympy import Symbol, E, I, oo


def to_sympy(message):
    """
    Parses a string containing mathematical expressions into sympy syntax.

    :param message: A string (usually a discord text message) containing a
        mathematical expression.
    :type message: str
    :return: The parsed expression.
    """
    transformations = (standard_transformations +
                       (implicit_multiplication_application, convert_xor,
                        split_symbols)
                       )
    custom_variables = {"inf": oo, "lol": Symbol("lol"), "e": E, "i": I}
    return parse_expr(message, transformations=transformations,
                      local_dict=custom_variables)



