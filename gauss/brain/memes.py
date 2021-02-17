"""Contains functions for sending, adding and removing memes"""
from os.path import join

from datetime import datetime

import discord

from gauss._utils import load_obj, save_obj
from gauss._physicists import PHYSICISTS
from gauss.webscraping.reddit import get_meme
OBJS = join(__file__.split("brain")[0], "_obj")
ADMINS = [PHYSICISTS["KENO"]]

NO_ADMIN_ERRMSG = "Dafür musst du ein geiler Macker sein"

SEXY_EINSTEIN = "https://i.redd.it/hcumvmngjto11.jpg"


class Meme:
    """Base class for memes"""
    def __init__(self, url, author):
        self.url = url
        self.author = author
        self.month = datetime.today().month
        self.rating = dict()

    def get_author(self):
        return self.author

    def get_url(self):
        return self.url

    def get_month(self):
        return self.month

    def get_rating(self, average=True):
        """
        Returns the average rating in the last two weeks.
        :return: The average rating.
        :rtype: float
        """
        today = datetime.today()
        this_month = today.month
        this_year = today.year
        rating = 0
        total_ratings = 0
        if this_year not in self.rating.keys():
            if average:
                return 0
            else:
                return 0, 0
        if this_month in self.rating[this_year].keys():
            rating = self.rating[this_year][this_month][0]
            total_ratings = self.rating[this_year][this_month][1]
        if average:
            return rating / total_ratings if total_ratings else 0
        else:
            return rating, total_ratings

    def rate(self, rating):
        """
        Adds a new rating to the meme.

        :param rating: A rating between 0 and 5
        :type rating: int
        """
        today = datetime.today()
        this_year = today.year
        this_month = today.month

        if this_year in self.rating.keys():
            if this_month in self.rating[this_year].keys():
                self.rating[this_year][this_month][0] += rating
                self.rating[this_year][this_month][1] += 1
            else:
                self.rating[this_year][this_month] = [rating, 1]
        else:
            self.rating[this_year] = {this_month: [rating, 1]}


def send_meme(message):
    """
    Sends a meme from a list of meme links

    :param message: A discord text message containing the word meme.
    :type message: :class:`discord.message.Message`
    :return: The message to send.
    """
    tag = _find_meme_tag(message, "send")
    members = load_obj(join(OBJS, "members.pkl"))
    recent_memes = members[message.author.id]["recent_memes"]

    if "fresh" in tag:
        meme_url = get_meme(tag.replace("fresh", "").strip())
        if meme_url is not None:
            meme = Meme(meme_url, "0")
            _add_to_recent_memes(meme, message, members)
            return message.channel.send(meme_url)
        else:
            return message.channel.send("Ich konnte kein Meme finden.")

    memes = load_obj(join(OBJS, "memes.pkl"))
    if tag == "last":
        if recent_memes:
            meme = recent_memes[-1]
            return message.channel.send(meme.get_url())
        else:
            return message.channel.send("Ich glaube nicht, dass ich dir schon ein Meme geschickt habe.")
    if tag in memes.keys():
        meme = _find_fresh_meme(memes[tag], message, members)
        return message.channel.send(meme)
    else:
        return message.channel.send("Ich konnte keine {} Memes finden.".format(tag))


def _find_fresh_meme(memes, message, members, sort_by_rating=True):
    """
    Finds a fresh meme that is not in the list of the last 10 displayed memes.

    :param memes: A list of memes to choose from
    :type memes: list
    :param message: A discord text message to find out the authors id.
    :type message: :class:`discord.message.Message`
    :param members: All the members that wrote a message to gauss.
    :type members: dict
    :return: The url of a fresh meme.
    :rtype: str
    """
    rated_memes = members[message.author.id]["rated_memes"].keys()
    recent_memes = [m.url for m in members[message.author.id]["recent_memes"]]

    memes_sorted_by_rating = sorted(memes, key=lambda m: m.get_rating(), reverse=True)

    for meme in memes_sorted_by_rating:
        if meme.get_url() not in recent_memes and meme.url not in rated_memes:
            _add_to_recent_memes(meme, message, members)
            return meme.get_url()
    return "Du hast bereits alle meine Memes gesehen"


def _find_best_meme(new_memes):
    """
    Finds the best ranked meme of a sample.
    :param new_memes: A list of meme objects.
    :return: The index of the best meme.
    """
    ratings = [m.get_rating() for m in new_memes]
    best_meme_index = ratings.index(max(ratings))
    return new_memes[best_meme_index]


def _add_to_recent_memes(meme, message, members):
    """
    Adds a meme to the recently displayed memes.

    :param meme: The url of the meme.
    :type meme: Meme
    :param message: A discord text message to find out the authors id.
    :type message: :class:`discord.message.Message`
    :param members: All the members that wrote a message to gauss.
    :type members: dict
    """
    recent_memes = members[message.author.id]["recent_memes"]
    members[message.author.id]["recent_memes"] = recent_memes[1:] + [meme]
    save_obj(members, join(OBJS, "members.pkl"))


def add_meme(message):
    """
    Adds a meme to the list of memes.

    :param message: A discord text message containing the word meme.
    :type message: :class:`discord.message.Message`
    :return: The message to send.
    """
    tag = _find_meme_tag(message, "add")
    meme_file_path = join(OBJS, "memes.pkl")
    members = load_obj(join(OBJS, "members.pkl"))
    recent_memes = members[message.author.id]["recent_memes"]

    if tag == "last":
        tag = message.content.split("meme")[1].replace("to", "").strip()
        if not tag:
            tag = "no-tag"
        meme_url = recent_memes[-1].get_url()
    else:
        meme_url = message.content.split("meme")[1].strip()

    msg = _add_meme(message, members, meme_file_path, meme_url, recent_memes, tag)
    return message.channel.send(msg + meme_url)


def _add_meme(message, members, meme_file_path, meme_url, recent_memes, tag):
    """
    Adds a meme to the collection.

    :param message: A discord text message.
    :param members: User information.
    :param meme_file_path: Url of the meme.
    :param meme_url: The url of the meme.
    :param recent_memes: The recent memes of the user.
    :param tag: A tag for the meme.
    :return:
    """
    memes = load_obj(meme_file_path)
    msg = "Das kenne ich schon."
    new_meme = Meme(meme_url, str(message.author.id))
    if tag not in memes.keys():
        memes[tag] = [new_meme]
    elif new_meme.get_url() not in [m.url for m in memes[tag]]:
        memes[tag].append(new_meme)
    else:
        return msg
    save_obj(memes, meme_file_path)
    _add_to_recent_memes(new_meme, message, members, recent_memes)
    msg = "Ich habe dieses Meme in meine Sammlung aufgenommen\n"
    return msg


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
            meme_urls = [m.get_url() for m in memes[tag]]
            wrong_meme_index = meme_urls.index(meme_path)
        except ValueError:
            continue
        else:
            user_id = message.author.id
            if memes[tag][wrong_meme_index].get_author() != str(user_id) and user_id not in ADMINS:
                return message.channel.send(NO_ADMIN_ERRMSG)
            else:
                del memes[tag][wrong_meme_index]
                break
    else:
        return message.channel.send("Das Meme kenne ich gar nicht.")
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
    last_meme = load_obj(join(OBJS, "members.pkl"))[message.author.id]["recent_memes"][-1]
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
    today = datetime.today()
    this_month = today.month
    members_path = join(OBJS, "members.pkl")
    memes_path = join(OBJS, "memes.pkl")
    members = load_obj(members_path)
    meme = members[message.author.id]["recent_memes"][-1]
    memes = load_obj(memes_path)

    if meme.get_url() in members[message.author.id]["rated_memes"].keys():
        if members[message.author.id]["rated_memes"][meme.get_url()][0] == this_month:
            rating = members[message.author.id]["rated_memes"][meme.get_url()][1]
            return message.channel.send("Das Meme hast du diesen Monat bereits mit {} bewertet.".format(rating))

    rating = _find_rating(message)

    for tag in memes.keys():
        try:
            meme_urls = [m.url for m in memes[tag]]
            rate_meme_idx = meme_urls.index(meme.url)
        except ValueError:
            continue
        else:
            memes[tag][rate_meme_idx].rate(rating)

    members[message.author.id]["rated_memes"][meme.get_url()] = (this_month, rating)
    save_obj(members, members_path)
    save_obj(memes, memes_path)
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
    memes = load_obj(join(OBJS, "memes.pkl"))

    top_memes = [("", 0)] * 5
    total_votes = 0

    for tag in memes.keys():
        for meme in memes[tag]:
            votes = meme.get_rating(average=False)[1]
            total_votes += votes
            if votes < 2:
                continue

            avg_rating = meme.get_rating()
            for idx, top_meme in enumerate(top_memes):
                if avg_rating > top_meme[1]:
                    if idx + 1 < 5:
                        top_memes[idx + 1] = top_memes[idx]
                    top_memes[idx] = (meme.get_url(), avg_rating)
                    break

    msg = "\n".join(("Hier sind die Top Memes dieses Monats!",
                     "insgesamt wurde {}mal gevoted",
                     "(Es werden nur Memes mit drei oder mehr Votes berücksichtigt)"))
    await message.channel.send(msg.format(total_votes))

    for idx, top_meme in enumerate(top_memes):
        if not top_meme[0]:
            await message.channel.send("Es gab nicht genügend Votes.")
            break
        await message.channel.send("Platz {} mit einer Gesamtwertung von {:.2f}\n".format(idx + 1, top_meme[1]))
        await message.channel.send(top_meme[0])
