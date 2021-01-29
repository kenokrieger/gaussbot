"""Module for saving a latex expression to a png file"""
from matplotlib.pyplot import rcParams, figure, close
from sympy import latex

custom_preamble = {
    "text.usetex": True,
    "text.latex.preamble": r"\usepackage{amsmath}"
    }
rcParams.update(custom_preamble)


def save_as_png(expr, filename, dpi=300):
    """
    Saves a sympy expression as a png with the help of matplotlib.

    :param expr: A sympy expression that shall be displayed.
    :type expr: sympy.core
    :param filename: The path where the figure will be saved to.
    :type filename: str or path
    :param dpi: The resolution of the image in dots per inch
    :type dpi: int
    """
    discord_background_color = "#36393F"
    fig = figure(facecolor=discord_background_color)
    fig.text(0, 0, r'${}$'.format(latex(expr)), color="white")
    fig.savefig(filename, dpi=dpi, bbox_inches='tight')
    close()
