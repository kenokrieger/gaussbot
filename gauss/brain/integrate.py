"""Contains functions for integrating the content of a message"""
from os.path import join

from sympy import integrate, Integral, simplify, Symbol, oo, E, Add

from gauss.rendering import save_as_png
from gauss.parse import to_sympy

PREVIEWS = join(__file__.split("brain")[0], '_previews')
VIEW_INPUT = join(PREVIEWS, 'input.png')
VIEW_OUTPUT = join(PREVIEWS, 'output.png')

X = Symbol('X')
GAUSSIAN_INTEGRAL = Integral(E ** (-X ** 2), (X, -oo, oo))

NO_INTVAR_DECLARED_ERRMSG = "Meine Güte willst du vielleicht noch mehr" \
                            " Variablen verwenden?! Für welche von denen " \
                            "soll ich das denn integrieren?\n Such dir eine" \
                            " aus: {}"


def do_integration(message, response=None):
    """
    Integrate a mathematical expression.

    :param message: A discord message containing the expression to integrate.
    :type message: :class:`discord.message.Message`
    :param response: If no integration variable was declared previously
        response will contain all the information from the previous attempt
        as well as the integration variable.
    :type response: dict
    """
    if response is None:
        integral = message.content.split('integrate')[1]
        integral, intvar = _find_intvar(integral)

        if _isdefinite(integral):
            integrand, limits = _sep_integrand(integral)
        else:
            integrand = to_sympy(integral)
            limits = None

        variables = integrand.free_symbols
        if intvar is None:
            if len(variables) > 1:
                question = NO_INTVAR_DECLARED_ERRMSG.format(variables)
                response = {"raise": message.channel.send(question),
                            "integrand": integrand, "limits": limits,
                            "gauss": False}
                return response
            else:
                (intvar, ) = variables
    else:
        integrand = response["integrand"]
        intvar = response["intvar"]
        limits = response["limits"]
    if _is_gaussian_integral(integrand, intvar, limits):
        return {"gauss": True}
    _save_integral_input(integrand, intvar, limits=limits)
    _integration(integrand, intvar, limits)


def integration_was_successful(response):
    """Checks whether the integration was successful or not by observing the
    returned response"""
    return True if response is None else False


def _is_gaussian_integral(integrand, intvar, limits):
    """
    Compares the input integral to the gaussian integral by subtracting
    both.

    :param integrand: The integrand of the integral.
    :param intvar: The integration variable.
    :param limits: The limits of the integral.
    :return: True for the gaussian integral False otherwise.
    """
    if limits is None:
        return False
    current_integral = Integral(integrand, (intvar, limits[0], limits[1]))
    if simplify(current_integral - GAUSSIAN_INTEGRAL) == 0:
        return True
    else:
        return False


def _isdefinite(message):
    """
    Checks whether the inquiry is a indefinite or definite integral.

    Args:
        message(str): The message to check.

    Returns:
        bool: True for a definite integral and False for an indefinite
            integral.

    """
    return 'from' in message


def _sep_integrand(integral):
    """
    Extracts integrand and limits from an integral expression.

    Args:
        integral(str): Expression containing integrand and limits.

    Returns:
        tuple: The integrand and the limits as a tuple

    """
    integrand = to_sympy(integral.split('from')[0])
    limits = integral.split('from')[1].split('to')
    lower_bound = to_sympy(limits[0])
    upper_bound = to_sympy(limits[1])
    limits = (lower_bound, upper_bound)

    return integrand, limits


def _find_intvar(message):
    """
    Checks whether an integration variable was declared in the message or not.

    :param message: An expression that might contain an integration variable.
    :type message: str
    :return: The modified message without the integration variable and
        if found the integration variable else None.
    :rtype: tuple
    """
    variable_declarer = [',', 'with respect to', 'd']

    for delimiter in variable_declarer:
        if delimiter in message:
            content = message.split(delimiter)
            if 'from' in content[1]:
                subcontent = content[1].split('from')
                intvar = to_sympy(subcontent[0])
                message = content[0] + 'from ' + subcontent[1]
                return message, intvar
            else:
                return content[0], to_sympy(content[1])
    return message, None


def _integration(integrand, variable, limits=None):
    """
    Integrates a given expression for each variable and
    returns a string containing all solutions as a result

    Args:
        integrand(sympy.object): The integrand.
        limits(tuple): The lower and upper bound of the integral defaults to
            None meaning the indefinite integral will be computed.

    """
    if limits is None:
        result = Add(integrate(integrand, variable),
                     Symbol("C", commutative=False))
    else:
        result = integrate(integrand, (variable, limits[0], limits[1]))
    save_as_png(result, VIEW_OUTPUT)


def _save_integral_input(integrand, intvar, limits=None):
    """
    Saves the given input as a png.

    :param integrand: The integrand of an integral.
    :type integrand: sympy.core object
    :param intvar: The integration variable.
    :type intvar: sympy.core object
    :param limits: The limits for the integration. Defaults to None.
    :type limits: tuple
    """
    if limits is not None:
        save_as_png(Integral(integrand, (intvar, limits[0], limits[1])),
                    VIEW_INPUT)
    else:
        save_as_png(Integral(integrand, intvar), VIEW_INPUT)
