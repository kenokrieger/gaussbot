"""Contains functions for finding out which task the brain shall perform"""
import discord
from os.path import join

from gauss import brain
from gauss.parse import to_sympy

VALID_CHANNELS = ["gauss", "troll", "Allgemein", "unterricht"]
GREETING_KEYWORDS = ["hi", "moin", "hallo", "tag", "hey", "Ni hao", "privjet",
                     "Konnichiwa", "Bonjour", "привет", "こんいちわ", "こんにちは",
                     "Это отлично!"]
PREVIEWS = join(__file__[:-14], '_previews')
VIEW_INPUT = join(PREVIEWS, 'input.png')
VIEW_OUTPUT = join(PREVIEWS, 'output.png')

GAUSSIAN_INTEGRAL_MSG = "Also wenn du das nicht kennst, kann ich dir auch nicht helfen."
NO_TASK_FOUND_ERRMSG = "Falls du etwas von mir wolltest habe ich es nicht verstanden"


def is_valid(message):
    """
    Validates that the received message is in the right channel and was not
    sent by a bot

    :param message: A discord text message.
    :type message: :class:`discord.message.Message`
    :return: `True` if the message is valid, `False` otherwise.
    :rtype: bool
    """
    if message.author.bot:
        return False
    elif isinstance(message.channel, discord.channel.DMChannel):
        return True
    elif message.channel.name in VALID_CHANNELS:
        return True
    else:
        return False


async def do_task(bot, message):
    """
    Searches through a message to find out if a task is to be performed and
    returns the result of that task.

    :param bot: The discord bot.
    :type bot: :class: `discord.Client`
    :param message: The message to search through.
    :type message: :class:`discord.message.Message`
    :return: The task to be performed and the message.
    :rtype: tuple
    """
    if "gauss" not in message.content.lower():
        return

    if "help" in message.content:
        await brain.show_help(message)
    elif "add meme" in message.content:
        await brain.add_meme(message)
    elif "remove meme" in message.content:
        await brain.remove_meme(message)
    elif "set greeting" in message.content:
        await brain.set_greeting(message)
    elif "declare var" in message.content:
        await brain.declare_custom_variable(message)
    elif "integrate" in message.content:
        await _coordinate_integration(bot, message)
    elif "diff" in message.content:
        await _coordinate_differentiation(bot, message)
    elif "calc" in message.content:
        await brain.do_calculation(message)
    elif "show" in message.content:
        await brain.show_latex(message)
    elif "send meme" in message.content:
        await brain.send_meme(message)
    elif "send nudes" in message.content:
        await brain.send_nudes(message)
    elif message.content.lower() in ['rip', 'r.i.p.']:
        await brain.pay_respect(message)
    elif any(greeting_keyword in message.content.lower() for greeting_keyword in GREETING_KEYWORDS):
        await brain.greet(message)
    else:
        await message.channel.send(NO_TASK_FOUND_ERRMSG)


async def _coordinate_differentiation(bot, message):
    """
    Coordinates the differentiation of an expression. This function will check
    whether a variable to differentiate for was specified and ask for one
    if that was not the case.

    :param bot: The discord bot.
    :type bot: :class: `discord.Client`
    :param message: The message with the content to differentiate.
    :type message: :class:`discord.message.Message`
    """
    response = brain.do_differentiation(message)
    if not brain.differentiation_was_successful(response):
        await response["raise"]
        answer = await bot.wait_for('message', check=check)
        response["diff_var"] = to_sympy(answer.content)
        brain.do_differentiation(message, response=response)
    await message.channel.send(
        'Das habe ich ja schon mit fünf abgeleitet!',
        file=discord.File(VIEW_INPUT))
    await message.channel.send(
        'TRIVIAL!',
        file=discord.File(VIEW_OUTPUT))


async def _coordinate_integration(bot, message):
    """
    Coordinates the integration of an expression. This function will check
    whether a integration variable was specified and ask for one if that was
    not the case.

    :param bot: The discord bot.
    :type bot: :class: `discord.Client`
    :param message: The message with the content to differentiate.
    :type message: :class:`discord.message.Message`
    """
    response = brain.do_integration(message)
    if not brain.integration_was_successful(response):
        if response["gauss"]:
            await message.channel.send(GAUSSIAN_INTEGRAL_MSG)
            return
        else:
            await response["raise"]
            answer = await bot.wait_for('message', check=check)
            response["intvar"] = to_sympy(answer.content)
            brain.do_integration(message, response=response)
    await message.channel.send(
        'Das Integral packst du nicht selber?!',
        file=discord.File(VIEW_INPUT))
    await message.channel.send(
        'TRIVIAL!',
        file=discord.File(VIEW_OUTPUT))


def check(message):
    return not message.author.bot and len(message.content) < 10
