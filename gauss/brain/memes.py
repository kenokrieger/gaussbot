"""Contains functions for sending, adding and removing memes"""
from os.path import join

from random import randint

from gauss._utils import load_obj, save_obj
from gauss._physicists import PHYSICISTS

OBJS = join(__file__.split("brain")[0], "obj")
ADMINS = [PHYSICISTS["KENO"]]
NO_ADMIN_ERRMSG = "Dafür musst du ein geiler Macker sein"

SEXY_EINSTEIN = "https://i.redd.it/hcumvmngjto11.jpg"


def send_meme(message):
    """
    Sends a meme from a list of meme links

    :param message: A discord text message containing the word meme.
    :type message: :class:`discord.message.Message`
    :return: The message to send.
    """
    memes = load_obj(join(OBJS, "memes.pkl"))
    recent_memes = load_obj(join(OBJS, "recent_memes.pkl"))
    meme = memes[randint(0, len(memes) - 1)]

    if meme in recent_memes:
        return send_meme(message)
    else:
        recent_memes = recent_memes[1:] + [meme]
        save_obj(recent_memes, join(OBJS, "recent_memes.pkl"))
        return message.channel.send(meme)


def add_meme(message):
    """
    Adds a meme to the list of memes.

    :param message: A discord text message containing the word meme.
    :type message: :class:`discord.message.Message`
    :return: The message to send.
    """
    save_file_path = join(OBJS, "memes.pkl")
    memes = load_obj(save_file_path)
    meme_path = message.content.split("add meme")[1].strip()
    if meme_path not in memes:
        memes.append(meme_path)
        save_obj(memes, save_file_path)
        msg = "Ich habe dieses Meme in meine Sammlung aufgenommen\n"
    else:
        msg = "Das kenne ich schon."
    return message.channel.send(msg + meme_path)


def remove_meme(message):
    """
    Adds a meme to the list of memes.

    :param message: A discord text message containing the word meme.
    :type message: :class:`discord.message.Message`
    :return: The messages to send.
    """
    if message.author.id not in ADMINS:
        return message.channel.send(NO_ADMIN_ERRMSG)
    save_file_path = join(OBJS, "memes.pkl")
    memes = load_obj(save_file_path)
    meme_path = message.content.split("remove meme")[1].strip()
    try:
        wrong_meme_index = memes.index(meme_path)
    except ValueError:
        return message.channel.send("Das Meme kenne ich gar nicht.")
    else:
        del memes[wrong_meme_index]
    save_obj(memes, save_file_path)
    msg = "Ich habe das Meme aus meiner Sammlung entfernt"
    return message.channel.send(msg)


def send_nudes(message):
    """Two words: sexy Einstein"""
    return message.channel.send(SEXY_EINSTEIN)


def pay_respect(message):
    """
    F in the chat

    :return: Respect
    """
    return message.channel.send('F')
