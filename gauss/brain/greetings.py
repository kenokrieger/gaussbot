"""Hello there"""
from os.path import join

from gauss._utils import save_obj, load_obj

OBJS = join(__file__.split("brain")[0], "_obj")


def greet(message):
    """
    Greets the user that sends a greeting to the bot depending on
    the users id.

    :param message: A discord message containing a greeting.
    :type message: :class:`discord.message.Message`
    :return: The appropriate response
    """
    members = load_obj(join(OBJS, "members.pkl"))
    response = members[message.author.id]["greeting"]
    return message.channel.send(response)


def set_greeting(message):
    """
    Changes the build-in greeting to a custom greeting.

    :param message: A discord text message containing 'set greeting'.
    :type message: :class:`discord.message.Message`
    """
    members_path = join(OBJS, "members.pkl")
    members = load_obj(members_path)
    new_greeting = message.content.split("set greeting")[1].strip()
    members[message.author.id]["greeting"] = new_greeting
    save_obj(members, members_path)

    return message.channel.send("Ich habe die neue Begrüßung für dich als: '{}' gesetzt".format(new_greeting))
