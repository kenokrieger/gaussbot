from os import getenv
from os.path import join
import traceback

import discord
from dotenv import load_dotenv

from gauss.coordinator import is_valid, find_task
from gauss.parse import to_sympy
from gauss.brain import greet, do_integration, pay_respect, show_latex, \
    integration_was_successful

load_dotenv()
TOKEN = getenv("DISCORD_TOKEN")
GUILD = getenv("DISCORD_GUILD")
PREVIEWS = join(__file__[:-6], '_previews')
VIEW_INPUT = join(PREVIEWS, 'input.png')
VIEW_OUTPUT = join(PREVIEWS, 'output.png')
GAUSSIAN_INTEGRAL_MSG = "Mhh, das ist ein schwerer Brocken. Ein guter " \
                        "Mathematiker könnte dir damit vielleicht " \
                        "weiterhelfen\n Ich habe gehört, daraus ein " \
                        "zweidimensionales Integral zu machen soll helfen."


class GaussBot(discord.Client):
    """The almighty gauss bot"""

    async def on_ready(self):
        """Searches for the bot connections on start"""
        guild = discord.utils.get(self.guilds, name=GUILD)
        print('{} is connected to {}'.format(self.user, guild.name))

    async def on_message(self, message):
        """
        Coordinates what happens once a message is received.

        :param message: The content of the message.
        :type message: str
        """
        with open('discord_IDs.txt', 'a') as f:
            try:
                f.write("{}:{}\n".format(message.author.name,
                                         message.author.id))
            except UnicodeEncodeError:
                pass

        if not is_valid(message):
            return

        try:
            task = find_task(message)
            if task == "greet":
                await greet(message)
            elif task == "pay respect":
                await pay_respect(message)
            elif task == "show":
                await show_latex(message)
            elif task == "integrate":
                response = do_integration(message)
                if not integration_was_successful(response):
                    if response["gauss"]:
                        await message.channel.send(GAUSSIAN_INTEGRAL_MSG)
                        return
                    else:
                        await response["raise"]
                        answer = await self.wait_for('message')
                        response["intvar"] = to_sympy(answer.content)
                        do_integration(message, response=response)

                await message.channel.send(
                    'Das Integral packst du nicht selber?!',
                    file=discord.File(VIEW_INPUT))
                await message.channel.send(
                    'TRIVIAL!',
                    file=discord.File(VIEW_OUTPUT))
            else:
                if message.attachments.first():
                    print(message.attachments.first().filename)
        except:
            err_msg = traceback.format_exc()
            with open("log.txt", 'a') as f:
                f.write(err_msg + '\n')
            await message.channel.send("Mhh, ich habe dich nicht verstanden. "
                                       "Das könnte das Resultat eines internen"
                                       " Fehlers sein, oder du hast dich bei"
                                       " deiner Eingabe vertippt.")
