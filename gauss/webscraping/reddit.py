from os import getenv
from dotenv import load_dotenv
import praw

from prawcore.exceptions import NotFound
load_dotenv()


def get_meme(tag):
    """
    Gets a random meme from reddit.

    :param tag: The genre of the meme.
    :return: None if no meme was found else the url to the meme.
    """
    reddit = praw.Reddit(client_id=getenv("CLIENT_ID"),
                         client_secret=getenv("CLIENT_SECRET"),
                         password=getenv("CLIENT_PASSWORD"),
                         user_agent=getenv("USER_AGENT"),
                         username=getenv("USERNAME"))

    try:
        subreddit = reddit.subreddit(tag + "memes")
    except NotFound:
        return

    meme = subreddit.random()
    return meme.url
