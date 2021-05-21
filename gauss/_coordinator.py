"""Contains functions for finding out which task the brain shall perform"""
import discord
from os.path import join

from gauss._utils import load_obj, save_obj
from gauss import brain
from gauss.parse import to_sympy
from gauss.brain.memes import Meme

VALID_CHANNELS = ["gauss", "troll", "Allgemein", "unterricht", "top-memes"]
GREETING_KEYWORDS = ["hi", "moin", "hallo", "tag", "hey", "Ni hao", "privjet",
                     "Konnichiwa", "Bonjour", "привет", "こんいちわ", "こんにちは",
                     "Это отлично!"]
PREVIEWS = join(__file__[:-15], '_previews')
OBJS = join(__file__.split("_coordinator.py")[0], "_obj")

VIEW_INPUT = join(PREVIEWS, 'input.png')
VIEW_OUTPUT = join(PREVIEWS, 'output.png')

GAUSSIAN_INTEGRAL_MSG = "Willst du mich auf den Arm nehmen?"
NO_TASK_FOUND_ERRMSG = "Falls du etwas von mir wolltest habe ich es nicht verstanden"

TASKS = {
    # 'command': (function, number of arguments)
    "help": (brain.subroutines.show_help, 1),
    "rate meme": (brain.memes.rate_meme, 1),
    "meme report": (brain.memes.meme_report, 1),
    "add meme": (brain.memes.add_meme, 1),
    "remove meme": (brain.memes.remove_meme, 1),
    "set meme tag": (brain.memes.set_meme_tag, 1),
    "set greeting": (brain.greetings.set_greeting, 1),
    "declare var": (brain.subroutines.declare_custom_variable, 1),
    "calc": (brain.subroutines.do_calculation, 1),
    "show": (brain.subroutines.show_latex, 1),
    "send meme": (brain.memes.send_meme, 1),
    "send nudes": (brain.memes.send_nudes, 1),
    "rip": (brain.memes.pay_respect, 1),
    "r.i.p.": (brain.memes.pay_respect, 1),
    "set status": (brain.subroutines.set_status, 2)
}

for greeting_keyword in GREETING_KEYWORDS:
    TASKS[greeting_keyword] = brain.greetings.greet


def is_valid(message):
    """
    Validates that the received message is in the right channel and was not
    sent by a bot

    :param message: A discord text message.
    :type message: :class:`discord.message.Message`
    :return: `True` if the message is valid, `False` otherwise.
    :rtype: bool
    """
    message_in_dm_channel = isinstance(message.channel, discord.channel.DMChannel)
    message_in_valid_channel = message.channel.name in VALID_CHANNELS
    is_bot = message.author.bot

    if (message_in_dm_channel or message_in_valid_channel) and not is_bot:
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

    members_path = join(OBJS, "members.pkl")
    members = load_obj(members_path)
    if message.author.id not in members.keys():
        greeting = "Hi! Du kannst dir mit dem Befehl set greeting" \
                   " eine persönliche Begrüßung einstellen."
        members[message.author.id] = {"greeting": greeting,
                                      "rated_memes": {},
                                      "recent_memes": [Meme("", "0")] * 30,
                                      "last_task": ""}
        save_obj(members, members_path)

    for key in TASKS:
        if key in message.content.lower():
            number_of_expected_args = TASKS[key][1]
            if number_of_expected_args == 1:
                await TASKS[key](message)
            elif number_of_expected_args == 2:
                await TASKS[key](bot, message)

    # the more complex tasks can't be mapped with a dictionary
    if message.content == "gauss -r":
        await _coordinate_last_task(members, bot, message)
        return
    elif "integrate" in message.content:
        await _coordinate_integration(bot, message)
    elif "diff" in message.content:
        await _coordinate_differentiation(bot, message)
    else:
        await message.channel.send(NO_TASK_FOUND_ERRMSG)
        return

    members = load_obj(members_path)
    members[message.author.id]["last_task"] = message.content
    save_obj(members, members_path)


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
    response = brain.differentiate.do_differentiation(message)
    if not brain.differentiate.differentiation_was_successful(response):
        await response["raise"]
        answer = await bot.wait_for('message', check=check)
        response["diff_var"] = to_sympy(answer.content)
        brain.differentiate.do_differentiation(message, response=response)
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
    response = brain.integrate.do_integration(message)
    if not brain.integrate.integration_was_successful(response):
        if response["gauss"]:
            await message.channel.send(GAUSSIAN_INTEGRAL_MSG)
            return
        else:
            await response["raise"]
            answer = await bot.wait_for('message', check=check)
            response["intvar"] = to_sympy(answer.content)
            brain.integrate.do_integration(message, response=response)
    await message.channel.send(
        'Das Integral packst du nicht selber?!',
        file=discord.File(VIEW_INPUT))
    await message.channel.send(
        'TRIVIAL!',
        file=discord.File(VIEW_OUTPUT))


async def _coordinate_last_task(members, bot, message):
    """
    Repeats the last task that was performed.

    :param members: User info.
    :param bot: The discord bot.
    :param message: A discord text message.
    """
    if "last_task" in members[message.author.id]:
        message.content = members[message.author.id]["last_task"]
        await do_task(bot, message)
    else:
        await message.channel.send("Du hast noch nicht mit mir gesprochen")


def check(message):
    return not message.author.bot and len(message.content) < 10
