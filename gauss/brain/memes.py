"""Contains functions for sending, adding and removing memes"""
from os.path import join

from random import randint
from datetime import datetime, timedelta
import calendar

import discord

from gauss._utils import load_obj, save_obj
from gauss._physicists import PHYSICISTS

OBJS = join(__file__.split("brain")[0], "_obj")
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
    tag = _find_meme_tag(message, "send")
    memes = load_obj(join(OBJS, "memes.pkl"))
    recent_memes = load_obj(join(OBJS, "recent_memes.pkl"))

    if tag in memes.keys():
        meme = _find_fresh_meme(memes[tag], recent_memes)
        return message.channel.send(meme)
    else:
        return message.channel.send("Ich konnte keine {} Memes finden.".format(tag))


def _find_fresh_meme(memes, recent_memes):
    """
    Finds a fresh meme that is not in the list of the last 10 displayed memes.

    :param memes: A list of memes to choose from
    :type memes: list
    :param recent_memes: The recent 10 memes.
    :type recent_memes: list
    :return: The url of a fresh meme.
    :rtype: str
    """
    meme = memes[randint(0, len(memes) - 1)]
    if meme in recent_memes:
        if len(memes) > 10:
            return _find_fresh_meme(memes, recent_memes)
        else:
            return meme
    else:
        _add_to_recent_memes(meme, recent_memes)
        return meme


def _add_to_recent_memes(meme, recent_memes):
    """
    Adds a meme to the recently displayed memes.

    :param meme: The url of the meme.
    :type meme: str
    :param recent_memes: List of the last 10 memes.
    :type recent_memes: list
    """
    recent_memes = recent_memes[1:] + [meme]
    save_obj(recent_memes, join(OBJS, "recent_memes.pkl"))


def add_meme(message):
    """
    Adds a meme to the list of memes.

    :param message: A discord text message containing the word meme.
    :type message: :class:`discord.message.Message`
    :return: The message to send.
    """
    tag = _find_meme_tag(message, "add")
    meme_file_path = join(OBJS, "memes.pkl")
    recent_memes = load_obj(join(OBJS, "recent_memes.pkl"))
    memes = load_obj(meme_file_path)
    meme_path = message.content.split("add meme")[1].strip()
    if meme_path not in memes.values():
        if tag not in memes.keys():
            memes[tag] = [meme_path]
        else:
            memes[tag].append(meme_path)
        save_obj(memes, meme_file_path)
        _add_to_recent_memes(meme_path, recent_memes)
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

    for tag in memes.keys():
        try:
            wrong_meme_index = memes[tag].index(meme_path)
        except ValueError:
            return message.channel.send("Das Meme kenne ich gar nicht.")
        else:
            del memes[tag][wrong_meme_index]
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


def _find_meme_tag(message, keyword):
    """
    Finds the meme tag of a message or returns \"no-tag\" if no tag was
    found.

    :param message: A discord text message that contains a tag for a meme.
    :type message: :class:`discord.message.Message`
    :return: The found tag or \"no-tag\"
    :rtype: str
    """
    tag = message.content.split(keyword)[1].split("meme")[0].strip().lower()
    return tag if tag else "no-tag"


def rate_meme(message):
    """
    Adds the meme rating to a dictionary.
    :param message: A discord text message.
    :type message: :class:`discord.message.Message`
    """
    date = datetime.today().date()
    meme_rating_path = join(OBJS, "meme_rating.pkl")
    meme = load_obj(join(OBJS, "recent_memes.pkl"))[-1]
    meme_ratings = load_obj(meme_rating_path)
    rating = _find_rating(message)
    if meme in meme_ratings.keys():
        ratings_by_day = meme_ratings[meme]
    else:
        ratings_by_day = {date: 0}
        meme_ratings[meme] = ratings_by_day

    if date in ratings_by_day.keys():
        meme_ratings[meme][date] += rating
    else:
        meme_ratings[meme][date] = rating
    save_obj(meme_ratings, meme_rating_path)
    return message.channel.send("Ich habe deine Wertung von {} aufgenommen.".format(rating))


def _find_rating(message):
    """
    Finds the rating for a meme from a message.

    :param message: A discord text message that contains a rating for a meme.
    :type message: :class:`discord.message.Message`
    :return: The found rating.
    :rtype: int
    """
    for number in range(6):
        if str(number) in message.content:
            break
    else:
        number = 0
    return number


def send_nudes(message):
    """Two words: sexy Einstein"""
    return message.channel.send(SEXY_EINSTEIN)


def pay_respect(message):
    """
    F in the chat

    :return: Respect
    """
    return message.channel.send('F')


async def meme_report(message):
    """
    Generates a meme report.

    :param message: A discord message asking for a meme report.
    :type message: :class:`discord.message.Message`
    :return: The memes to send.
    """
    if message.author.id not in ADMINS:
        return message.channel.send(NO_ADMIN_ERRMSG)

    meme_ratings = load_obj(join(OBJS, "meme_rating.pkl"))
    timeframe = message.content.split("meme report")[1].strip()
    time_interval = _find_date_interval(timeframe)

    top_memes = [("", 0)] * 5
    for meme in meme_ratings.keys():
        total_rating = 0
        for rate_date in meme_ratings[meme].keys():
            if time_interval[0].date() <= rate_date <= time_interval[1].date():
                total_rating += meme_ratings[meme][rate_date]
        for idx, top_meme in enumerate(top_memes):
            if total_rating > top_meme[1]:
                top_memes[idx] = (meme, total_rating)
                break

    await message.channel.send("Hier sind die Top Memes {} !".format(timeframe.capitalize()))

    for idx, top_meme in enumerate(top_memes):
        if not top_meme[0]:
            break
        await message.channel.send("Platz {} mit einer Gesamtwertung von {}\n".format(idx + 1, top_meme[1]))
        await message.channel.send(top_meme[0])


def _find_date_interval(timeframe):
    """
    Finds a date interval of either this or last week, month or year.

    :param timeframe: The desired timeframe.
    :type timeframe: str
    :return: The date interval.
    :rtype: tuple
    """
    today = datetime.today()

    if "week" in timeframe:
        if "last" in timeframe:
            today -= timedelta(days=7)
        return _this_week(today)
    elif "month" in timeframe:
        if "last" in timeframe:
            today = datetime(today.year, today.month - 1, today.day)
        return _this_month(today)
    elif "year" in timeframe:
        if "last" in timeframe:
            today -= timedelta(days=366)
        return _this_year(today)


def _this_week(today):
    """
    Finds the first and last day of this week.

    :param today: The date of today.
    :return: The first and last day of the week
    :rtype: tuple
    """
    monday = today
    for diff in range(7):
        date_to_check = today - timedelta(days=diff)
        if not date_to_check.weekday():
            monday = date_to_check
            break
    sunday = (monday + timedelta(days=6))
    return monday, sunday


def _this_month(today):
    """
    Finds the first and last day of this month.

    :param today: The date of today.
    :return: The first and last day of this month.
    :rtype: tuple
    """
    first_day_this_month = 1
    last_day_this_month = calendar.monthrange(today.year, today.month)[1]
    first_day = datetime(today.year, today.month, first_day_this_month)
    last_day = datetime(today.year, today.month, last_day_this_month)
    return first_day, last_day


def _this_year(today):
    """
    Finds the first and last day of this year.

    :param today: The date of today.
    :return: The first and last day of this year.
    :rtype: tuple
    """
    first_day = datetime(today.year, 1, 1)
    last_day = datetime(today.year, 12, 31)
    return first_day, last_day




