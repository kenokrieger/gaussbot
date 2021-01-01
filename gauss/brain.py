"""This is where all useful functions for the gauss bot are located"""
from os.path import join

from sympy import integrate, Integral, latex, diff
from matplotlib.pyplot import subplots
from gauss.parse import to_sympy
import matplotlib as mpl
mpl.rcParams['text.usetex'] = True
PREVIEWS: str = join(__file__[:-8], '_previews')


def do_integration(message):
    """
    Integrate a mathematical expression.

    Args:
        message(str): A string containing the expression to integrate.
    Returns:
        tuple: A status report, the integrated solution and the input.

    """
    integral = message.split('integrate')[1]
    integral, intvar = _find_intvar(integral)

    if _isdefinite(integral):
        integrand, limits = _sep_integrand(integral)

    else:
        integrand = to_sympy(integral)
        limits = None

    variables = integrand.free_symbols
    if intvar is None:
        if len(variables) > 1:
            answer = '\n'.join((
                'I\'m not sure with respect to what variable you expect me to integrate.',
                'You may chose one of the following: {}\n'.format(variables)
            ))
            return False, answer, integrand, limits

        else:
            (intvar, ) = variables

    if limits is not None:
        savepng(Integral(integrand, (intvar, limits[0], limits[1])), join(PREVIEWS, 'input.png'))
    else:
        savepng(Integral(integrand, intvar), join(PREVIEWS, 'input.png'))
    return True, _integration(integrand, intvar, limits), integrand, limits


def do_integration_again(integrand, variable, limits):
    """
    Follows up the do_integration function if no integration variable was found.

    Args:
        integrand(sympy.object):
        variable(str):
        limits(tuple):

    Returns
        sympy.object: The solution.

    """
    if limits is not None:
        savepng(Integral(integrand, (to_sympy(variable), limits[0], limits[1])), join(PREVIEWS, 'input.png'))
    else:
        savepng(Integral(integrand, to_sympy(variable)), join(PREVIEWS, 'input.png'))
    return _integration(integrand, to_sympy(variable), limits)


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


def savepng(expr, filename, dpi=100):
    """
    Saves a sympy expression as a png with help of matplotlib.
    :param expr:
    :param filename:
    :param dpi:
    :return:
    """
    fig, ax = subplots(frameon=False)
    ax.get_xaxis().set_visible(False)
    ax.get_yaxis().set_visible(False)
    render = fig.canvas.get_renderer()

    plottext = r'{}'.format(latex(expr)).replace(r'\sffamily', '').replace(r'\operatorname', r'\mathtt')
    if 'cases' in plottext:
        _caseplot(fig, ax, render, plottext)
    else:
        text = ax.text(0.05, 0.4, r'${}$'.format(plottext), fontsize=50)
        textdim = text.get_window_extent(renderer=render)

        fig.set_size_inches(textdim.width / 50, textdim.height / 50)
    fig.savefig(filename, dpi=dpi)


def _caseplot(fig, ax, render, plottext):
    """
    Plots the solution if multiple cases exist.
    :param fig:
    :param ax:
    :param plottext:
    :return:
    """

    clearstr = plottext.replace(r'\begin{cases}', '').replace(r'\end{cases}', '')\
        .replace('&', '').replace(r'\text', r'\mathtt')
    cases = clearstr.split(r'\\')

    ypos = -0.2
    heights = []
    widths = []

    for case in cases:
        ypos += 0.3
        text = ax.text(0.1, ypos, r'${}$'.format(case), fontsize=25)
        textdim = text.get_window_extent(renderer=render)
        heights.append(textdim.height / 20)
        widths.append(textdim.width / 50)

    fig.set_size_inches(max(widths), max(heights))


def _isdefinite(message):
    """
    Checks whether the inquiry is a indefinite or definite integral.

    Args:
        message(str): The message to check.

    Returns:
        bool: True for a definite integral and False for an indefinite integral.

    """
    return 'from' in message


def _find_intvar(message):
    """
    Checks whether an integration variable was declared in the message or not.

    Args:
        message(str): An expression that might contain an integration variable.

    Returns:
        tuple: The modified message that excludes the integration variable and
            if found the integration variable else None.

    """
    if 'd' in message:
        varindex = message.find('d') + 1
        intvar = to_sympy(message[varindex])
        message = message[:varindex - 1] + message[varindex + 1:]
        return message, intvar

    if ',' in message or 'with respect to' in message:
        delimiter = ',' if ',' in message else 'with respect to'
        content = message.split(delimiter)
        if 'from' in content[1]:
            subcontent = content[1].split('from')
            intvar = to_sympy(subcontent[0])
            message = content[0] + 'from ' + subcontent[1]
            return message, intvar
        else:
            return content[0], to_sympy(content[1])
    else:
        return message, None


def _integration(integrand, variable, limits=None):
    """
    Integrates a given expression for each variable and
    returns a string containing all solutions as a result

    Args:
        integrand(sympy.object): The integrand.
        limits(tuple): The lower and upper bound of the integral default to None meaning the
            indefinite integral will be computed.

    """
    if limits is None:
        result = integrate(integrand, variable)
    else:
        result = integrate(integrand, (variable, limits[0], limits[1]))
    savepng(result, join(PREVIEWS, 'output.png'))
    return result


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
