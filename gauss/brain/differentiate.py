"""Contains functions for differentiating the content of a message"""
from os.path import join

from sympy import diff, Derivative
from gauss.rendering import save_as_png
from gauss.parse import to_sympy

PREVIEWS = join(__file__.split("brain")[0], '_previews')
VIEW_INPUT = join(PREVIEWS, 'input.png')
VIEW_OUTPUT = join(PREVIEWS, 'output.png')

NO_DIFFVAR_DECLARED_ERRMSG = "Meine Güte willst du vielleicht noch mehr" \
                            " Variablen verwenden?! Für welche von denen " \
                            "soll ich das denn ableiten?\n Such dir eine" \
                            " aus: {}"


def do_differentiation(message, response=None):
    """
    Derivates an expression.

    :param message: A discord text message containing an expression to
        differentiate.
    :type message: :class:`discord.message.Message`
    :param response: Supplied if a previous differentiation failed.
    :type response: dict
    """
    if response is None:
        diff_part = message.content.split("diff")[1]
        diff_expr, diff_var = _find_diffvar(diff_part)

        if diff_var is None:
            variables = diff_expr.free_symbols

            if len(variables) > 1:
                question = NO_DIFFVAR_DECLARED_ERRMSG.format(variables)
                response = {"raise": message.channel.send(question),
                            "diff_expr": diff_expr}
                return response
            else:
                (diff_var,) = variables
    else:
        diff_expr = response["diff_expr"]
        diff_var = response["diff_var"]
    save_as_png(Derivative(diff_expr, diff_var), VIEW_INPUT)
    _differentiate(diff_expr, diff_var)


def _find_diffvar(diff_part):
    """
    Finds the variable to differentiate and expression for.

    :param diff_part: A string that contains an expression to differentiate.
    :type diff_part: str
    :return: The expression to differentiate and the variable for which to
        differentiate if found else returns None.
    :rtype: tuple
    """
    delimiters = [',', "with respect to"]
    for delimiter in delimiters:
        if delimiter in diff_part:
            split_diff = diff_part.split(delimiter)
            return to_sympy(split_diff[0]), to_sympy(split_diff[1])
    return to_sympy(diff_part), None


def _differentiate(expr, var):
    """
    Differentiates a given expression and saves the result as a png.

    :param expr: A sympy expression to differentiate
    :type expr: sympy.core
    :param var: The variable to differentiate for.
    :type var: sympy.core
    """
    save_as_png(diff(expr, var), VIEW_OUTPUT)


def differentiation_was_successful(response):
    """Checks whether the derivation was successful or not by observing the
    returned response.
    """
    return True if response is None else False
