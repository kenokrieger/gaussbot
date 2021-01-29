"""Module for saving a latex expression to a png file"""
from matplotlib.pyplot import figure, close
from sympy import latex


def savepng(expr, filename, dpi=100):
    """
    Saves a sympy expression as a png with help of matplotlib.
    :param expr:
    :param filename:
    :param dpi:
    :return:
    """
    fig = figure(facecolor="#36393F")
    render = fig.canvas.get_renderer()

    plottext = r'{}'.format(latex(expr)).replace(r'\sffamily', '').replace(
        r'\operatorname', r'\mathtt')
    if 'cases' in plottext:
        _caseplot(fig, render, plottext)
    else:
        text = fig.text(0.05, 0.4, r'${}$'.format(plottext), fontsize=50,
                       color="white")
        textdim = text.get_window_extent(renderer=render)

        fig.set_size_inches(textdim.width / 50, textdim.height / 50)
    fig.savefig(filename, dpi=dpi)
    close()


def _caseplot(fig, render, plottext):
    """
    Plots the solution if multiple cases exist.
    :param fig:
    :param plottext:
    :return:
    """
    clearstr = plottext.replace(r'\begin{cases}', '').replace(
        r'\end{cases}', '').replace('&', '').replace(r'\text', r'\mathtt')
    cases = clearstr.split(r'\\')

    ypos = -0.2
    heights = []
    widths = []

    for case in cases:
        ypos += 0.1
        pltext = fig.text(0.1, ypos, r'${}$'.format(case), fontsize=25,
                         color="white")
        textdim = pltext.get_window_extent(renderer=render)
        print(textdim.height)
        heights.append(textdim.height / 50)
        widths.append(textdim.width / 50)
    fig.set_size_inches(max(widths), sum(heights))
