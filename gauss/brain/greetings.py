"""Hello there"""
from os.path import join

from gauss._utils import save_obj, load_obj
from gauss._physicists import PHYSICISTS

OBJS = join(__file__.split("brain")[0], "_obj")

ADMINS = [PHYSICISTS["KENO"]]
NO_ADMIN_ERRMSG = "Dafür musst du ein geiler Macker sein"


def greet(message):
    """
    Greets the user that sends a greeting to the bot depending on
    the users id.

    :param message: A discord message containing a greeting.
    :type message: :class:`discord.message.Message`
    :return: The appropriate response
    """
    greetings = load_obj(join(OBJS, "greetings.pkl"))
    for physicist in PHYSICISTS.keys():
        if message.author.id == PHYSICISTS[physicist]:
            if physicist in greetings.keys():
                response = greetings[physicist]
            else:
                response = "Hi! Du kannst dir mit dem Befehl set greeting" \
                           " eine persönliche Begrüßung einstellen."
            break
    else:
        try:
            response = "Hi " + message.author.name
        except UnicodeEncodeError:
            response = "Hi"
    return message.channel.send(response)


def set_greeting(message):
    """
    Changes the build-in greeting to a custom greeting.

    :param message: A discord text message containing 'set greeting'.
    :type message: :class:`discord.message.Message`
    """
    greetings = load_obj(join(OBJS, "greetings.pkl"))

    for physicist in PHYSICISTS.keys():
        if physicist in message.content and message.author.id in ADMINS:
            key = physicist
            greetings[key] = message.content.replace(key, '').split(
                "set greeting")[1].strip()
            break
    else:
        for name, identity in PHYSICISTS.items():
            if message.author.id == identity:
                key = name
                greetings[key] = message.content.split(
                    "set greeting")[1].strip()
                break
        else:
            return message.channel.send("Dafür kennen wir uns noch nicht gut "
                                        "genug.")

    save_obj(greetings, join(OBJS, "greetings.pkl"))
    return message.channel.send("Ich habe die neue Begrüßung für {} als: '{}' "
                                "gesetzt".format(key.capitalize(),
                                                 greetings[key]))
