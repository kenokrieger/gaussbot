"""This is where all useful functions for the gauss bot are located"""
from sympy import Symbol, integrate
import parse


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
        integrand = parse.to_sympy(integral)
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
    return _integration(integrand, parse.to_sympy(variable), limits)


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
        intvar = parse.to_sympy(message[varindex])
        message = message[:varindex - 1] + message[varindex + 1:]
        return message, intvar

    if ',' in message:
        content = message.split(',')
        if 'from' in content[1]:
            subcontent = content[1].split('from')
            intvar = parse.to_sympy(subcontent[0])
            message = content[0] + 'from ' + subcontent[1]
            return message, intvar
        else:
            return content[0], parse.to_sympy(content[1])

    elif 'with respect to' in message:
        content = message.split('with respect to')
        return content[0], parse.to_sympy(content[1])

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
    return result


def _sep_integrand(integral):
    """
    Extracts integrand and limits from an integral expression.

    Args:
        integral(str): Expression containing integrand and limits.

    Returns:
        tuple: The integrand and the limits as a tuple

    """
    integrand = parse.to_sympy(integral.split('from')[0])
    limits = integral.split('from')[1].split('to')
    lower_bound = parse.to_sympy(limits[0])
    upper_bound = parse.to_sympy(limits[1])
    limits = (lower_bound, upper_bound)

    return integrand, limits
