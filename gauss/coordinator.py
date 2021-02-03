"""Contains functions for finding out which task the brain shall perform"""
import discord

VALID_CHANNELS = ["gauss", "troll", "Allgemein", "unterricht"]
GREETING_KEYWORDS = ["hi", "moin", "hallo", "tag", "hey", "Ni hao", "privjet",
                     "Konnichiwa", "Bonjour", "привет", "こんいちわ", "こんにちは",
                     "Это отлично!"]


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


def find_task(message):
    """
    Searches through a message to find out if a task is to be performed.

    :param message: The message to search through.
    :type message: :class:`discord.message.Message`
    :return: The task to be performed and the message.
    :rtype: tuple
    """
    if "gauss" not in message.content.lower():
        return ""

    if "help" in message.content:
        return "show help"

    if "set greeting" in message.content:
        return "set greeting"

    if "add meme" in message.content:
        return "add meme"

    if "remove meme" in message.content:
        return "remove meme"

    if "declare var" in message.content:
        return "set var"

    if "integrate" in message.content:
        return "integrate"

    if message.content.lower() in ['rip', 'r.i.p.']:
        return "pay respect"

    if "show" in message.content:
        return "show"

    if "calc" in message.content:
        return "calc"

    if "diff" in message.content:
        return "differentiate"

    if "send meme" in message.content:
        return "send meme"

    if "send nudes" in message.content:
        return "send nudes"
    for greeting_keyword in GREETING_KEYWORDS:
        if greeting_keyword in message.content.lower():
            return "greet"
