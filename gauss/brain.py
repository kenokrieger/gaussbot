"""This is where all useful functions for the gauss bot are located"""
from os.path import join
from sympy import integrate, Integral, diff, simplify, Symbol, oo, E

from gauss.parse import to_sympy
from gauss.rendering import save_as_png
from gauss._physicists import PHYSICISTS
from gauss.utils import load_obj, save_obj

import discord

PREVIEWS = join(__file__[:-8], '_previews')
OBJS = join(__file__[:-8], 'obj')
VIEW_INPUT = join(PREVIEWS, 'input.png')
VIEW_OUTPUT = join(PREVIEWS, 'output.png')
X = Symbol('X')
GAUSSIAN_INTEGRAL = Integral(E ** (-X ** 2), (X, -oo, oo))
NO_INTVAR_DECLARED_ERRMSG = "Meine Güte willst du vielleicht noch mehr" \
                            " Variablen verwenden?! Für welche von denen " \
                            "soll ich das denn integrieren?\n Such dir eine" \
                            " aus: {}"


def greet(message):
    """
    Greets the user that sends a greeting to the bot depending on
    the users id.

    :param message: A discord message containing a greeting.
    :type message: :class:`discord.message.Message`
    :return: The appropriate response
    :rtype: str
    """
    greetings = load_obj(join(OBJS, "greetings.pkl"))
    for physicist in PHYSICISTS.keys():
        if message.author.id == PHYSICISTS[physicist]:
            response = greetings[physicist]
            break
    else:
        try:
            response = "Hi " + message.author.name
        except UnicodeEncodeError:
            response = "Hi"
    return message.channel.send(response)


def set_greeting(message):
    """
    Changes the build in greeting to a custom greeting.

    :param message: A discord text message containing 'set greeting'.
    :type message: :class:`discord.message.Message`
    """
    greetings = load_obj(join(OBJS, "greetings.pkl"))

    for physicist in PHYSICISTS.keys():
        if physicist in message.content:
            key = physicist
            greetings[key] = message.content.replace(key, '').split(
                "set greeting")[1].strip()
            break
    else:
        for name, identity in PHYSICISTS.items():
            if message.author.id == identity:
                key = name
                greetings[key] = message.content.split(
                    "set greeting")[1].strip()
                break
        else:
            return message.channel.send("Dafür kennen wir uns noch nicht gut "
                                        "genug.")

    save_obj(greetings, join(OBJS, "greetings.pkl"))
    return message.channel.send("Ich habe die neue Begrüßung als: '{}' "
                                "gesetzt".format(greetings[key]))


def pay_respect(message):
    """
    F in the chat

    :return: Respect
    :rtype: str
    """
    return message.channel.send('F')


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
    _save_input(integrand, intvar, limits=limits)
    _integration(integrand, intvar, limits)


def integration_was_successful(response):
    """Checks whether the integration was successful or not by observing the
    returned response"""
    return True if response is None else False


def _is_gaussian_integral(integrand, intvar, limits):
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
        result = integrate(integrand, variable)
    else:
        result = integrate(integrand, (variable, limits[0], limits[1]))
    save_as_png(result, VIEW_OUTPUT)


def _save_input(integrand, intvar, limits=None):
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


def show_latex(message):
    """
    Creates an image out of a latex expression.

    :param message: A discord text message containing latex code.
    :type message: :class:`discord.message.Message`
    """
    latex_part = message.content.split("show")[1]
    save_as_png(latex_part, VIEW_OUTPUT, is_latex=True)
    return message.channel.send(file=discord.File(VIEW_OUTPUT))


def do_calculation(message):
    """
    Converts the given input into a float number and sends it back to the
    user.

    :param message: A discord text message containing something to evaluate.
    :type message: :class:`discord.message.Message`
    :return: The message to send.
    """
    calculation_part = message.content.split("calc")[1]
    calculation = to_sympy(calculation_part, numerical=True)
    return message.channel.send("{:.8E}".format(calculation))


def do_derivation(message):
    """
    Derivates an expression.
    :param message:
    :return:
    """
    deriv = message.split('diff')[1]
    derivative = to_sympy(deriv)
    variables = derivative.free_symbols

    if len(variables) > 1:
        return False, derivative
    else:
        (var, ) = variables
    solution = diff(derivative, var)
    return True, solution


def do_derivation_again(derivative, var):
    return diff(derivative, to_sympy(var))



