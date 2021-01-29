"""Module for saving a latex expression to a png file"""
from matplotlib.pyplot import rcParams, figure, close
from sympy import latex

custom_preamble = {
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}"
    }
rcParams.update(custom_preamble)


def save_as_png(expr, filename, is_latex=False, dpi=300):
    """
    Saves a sympy expression as a png with the help of matplotlib.

    :param expr: A sympy expression that shall be displayed.
    :type expr: sympy.core or latex str
    :param filename: The path where the figure will be saved to.
    :type filename: str or path
    :param is_latex: Specifies whether the string is already in latex format or
        needs to be parsed.
    :type latex: bool
    :param dpi: The resolution of the image in dots per inch
    :type dpi: int
    """
    discord_background_color = "#36393F"
    if is_latex:
        text = r"$\displaystyle" + r'{}$'.format(expr)
    else:
        text = r'${}$'.format(latex(expr))
    fig = figure(facecolor=discord_background_color)
    fig.text(0, 0, text, color="white")
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    close()
