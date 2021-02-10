"""Contains functions for sending, adding and removing memes"""
from os.path import join

from random import randint

import discord

from gauss._utils import load_obj, save_obj
from gauss._physicists import PHYSICISTS

OBJS = join(__file__.split("brain")[0], "_obj")
ADMINS = [PHYSICISTS["KENO"]]
MEME_TAGS = ["spicy", "physics", "dank", "gaming"]

NO_ADMIN_ERRMSG = "Dafür musst du ein geiler Macker sein"

SEXY_EINSTEIN = "https://i.redd.it/hcumvmngjto11.jpg"


def send_meme(message):
    """
    Sends a meme from a list of meme links

    :param message: A discord text message containing the word meme.
    :type message: :class:`discord.message.Message`
    :return: The message to send.
    """
    tag = message.content.split("send")[1].split("meme")[0].strip().lower()
    untagged_memes = load_obj(join(OBJS, "_memes.pkl"))
    tagged_memes = load_obj(join(OBJS, "memes.pkl"))
    recent_memes = load_obj(join(OBJS, "recent_memes.pkl"))

    if tag:
        if tag in tagged_memes.keys():
            memes = tagged_memes[tag]
        else:
            return message.channel.send("Ich konnte keine {} Memes finden.".format(tag))
    else:
        memes = untagged_memes

    meme = memes[randint(0, len(memes) - 1)]
    if meme in recent_memes:
        if len(memes) > 10:
            return send_meme(message)
        else:
            return message.channel.send(meme)
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
    save_file_path = join(OBJS, "_memes.pkl")
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
    save_file_path = join(OBJS, "_memes.pkl")
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


def set_meme_tag(message):
    """
    Adds a tag for the meme that was last displayed.

    :param message: A discord text message that contains a tag for a meme.
    :type message: :class:`discord.message.Message`
    :return: The answer gauss will send, confirming that the tag was added.
    """
    meme_path = join(OBJS, "memes.pkl")
    tag = message.content.lower().split("set meme tag")[1].strip()
    memes = load_obj(meme_path)
    last_meme = load_obj(join(OBJS, "recent_memes.pkl"))[-1]
    response = "Ich habe für das letzte Meme das Tag \'{}\' hinzugefügt.".format(tag)
    if tag not in memes.keys():
        memes[tag] = [last_meme]
    elif last_meme not in memes[tag]:
        memes[tag].append(last_meme)
    else:
        response = "Den Tag hat das Meme bereits."
    save_obj(memes, meme_path)
    return message.channel.send(response)


def rate_meme(message, meme):
    """
    Adds the meme rating to a dictionary.
    :param message: A discord text message.
    :param meme: The url of the meme.
    :return:
    """
    meme_rating_path = join(OBJS, "meme_rating.pkl")
    meme_rating = load_obj(meme_rating_path)
    memes = load_obj(join(OBJS, "_memes.pkl"))
    meme_ind = str(memes.index(meme))

    for grade in range(6):
        if str(grade) in message.content:
            rating = grade
        else:
            return

    if meme_ind not in meme_rating.keys():
        meme_rating[meme_ind] = rating
    else:
        meme_rating[meme_ind] += rating

    save_obj(meme_rating, meme_rating_path)


def send_nudes(message):
    """Two words: sexy Einstein"""
    return message.channel.send(SEXY_EINSTEIN)


def pay_respect(message):
    """
    F in the chat

    :return: Respect
    """
    return message.channel.send('F')
