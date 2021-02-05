"""Basically all leftover functions"""
from os.path import join

from sympy import Symbol

from gauss.parse import to_sympy
from gauss.rendering import save_as_png
from gauss._utils import save_obj, load_obj

import discord
import codecs

PREVIEWS = join(__file__.split("brain")[0], '_previews')
OBJS = join(__file__.split("brain")[0], "obj")
VIEW_OUTPUT = join(PREVIEWS, 'output.png')


def show_help(message):
    """Sends a help message"""
    with codecs.open(join(__file__[:-8], "help/commands.txt"), 'r', "utf-8") as f:
        msg = f.read()
    return message.channel.send(msg)


def declare_custom_variable(message):
    """
    Add a custom variable name to the dict for sympy's parsing.

    :param message: A discord text message containing 'declare var'.
    :type message: :class:`discord.message.Message`
    :return: The answer to send.
    """
    custom_variables = load_obj(join(OBJS, "custom_vars.pkl"))
    message_content = message.content.split("declare var")[1]
    custom_variable = "".join(message_content.split())

    if custom_variable in custom_variables.keys():
        return message.channel.send("Diese Variable kenne ich schon.")
    custom_variables[custom_variable] = Symbol(custom_variable)
    save_obj(custom_variables, join(OBJS, "custom_vars.pkl"))
    return message.channel.send("Ich habe {} in meinen Wortschatz"
                                " aufgenommen".format(custom_variable))


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
