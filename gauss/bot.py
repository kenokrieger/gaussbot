from os import getenv
from os.path import join
import traceback
import discord

from dotenv import load_dotenv

from gauss.coordinator import is_valid, do_task

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("DISCORD_GUILD")
PREVIEWS = join(__file__[:-6], '_previews')
VIEW_INPUT = join(PREVIEWS, 'input.png')
VIEW_OUTPUT = join(PREVIEWS, 'output.png')


class GaussBot(discord.Client):
    """The almighty gauss bot"""

    async def on_ready(self):
        """Searches for the bot connections on start"""
        guild = discord.utils.get(self.guilds, name=GUILD)
        print('{} is connected to {}'.format(self.user, guild.name))
        await self.change_presence(activity=discord.Game(
            name="Integral solving 101"))

    async def on_message(self, message):
        """
        Coordinates what happens once a message is received.

        :param message: A discord text message.
        :type message: :class:`discord.message.Message`
        """
        with open('discord_IDs.txt', 'a') as f:
            try:
                f.write("{}:{}\n".format(message.author.name,
                                         message.author.id))
            except UnicodeEncodeError:
                pass

        if not is_valid(message):
            return
        await do_task(self, message)

    async def error_log(self, message):
        err_msg = traceback.format_exc()
        with open("log.txt", 'a') as f:
            f.write(err_msg + '\n')
        await message.channel.send("Mhh, ich habe dich nicht verstanden. "
                                   "Das könnte das Resultat eines internen"
                                   " Fehlers sein, oder du hast dich bei"
                                   " deiner Eingabe vertippt.")
