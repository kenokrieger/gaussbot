"""Contains all the necessary parsers for discord messages"""
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, \
    implicit_multiplication_application, convert_xor, split_symbols
from sympy import Symbol, E, I, oo, N

CONSTANTS = {
    'c': 299792458,
    'e': 1.602176634e-19,
    'mu0': 1.25663706212e-6,
    'e0': 8.8541878128e-12,
    'G': 6.67430e-11,
    'kb': 1.380649e-23,
    'sigma': 5.670374419e-8,
    'Na': 6.02214076e23,
    'R': 8.31446261815324,
    'Rinf': 1.0973731568160e7,
    'h': 6.62607015e-34,
    'hbar': 1.054571817e-34,
    'me': 9.1093837015e-31,
    'a0': 5.29177210903e-11
}


def to_sympy(message, numerical=False):
    """
    Parses a string containing mathematical expressions into sympy syntax.

    :param message: A string (usually a discord text message) containing a
        mathematical expression.
    :type message: str
    :param numerical: States whether the solution shall be computed
        analytically or numerically.
    :type numerical: bool
    :return: The parsed expression.
    """
    transformations = (standard_transformations +
                       (implicit_multiplication_application, convert_xor,
                        split_symbols)
                       )

    custom_variables = {"inf": oo, "lol": Symbol("lol"), "i": I, "e": E,
                        "deineHose": Symbol("deineHose")}
    if not numerical:
        return parse_expr(message, transformations=transformations,
                          local_dict=custom_variables)
    else:
        custom_variables.update(CONSTANTS)
        return N(parse_expr(message, transformations=transformations,
                            local_dict=custom_variables))
