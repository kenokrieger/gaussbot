from os import getenv
from os.path import join

import discord
from dotenv import load_dotenv

from .brain import do_integration, do_integration_again, do_derivation,\
    do_derivation_again

load_dotenv()
TOKEN = getenv('DISCORD_TOKEN')
GUILD = getenv('DISCORD_GUILD')
KENO = int(getenv('KENO'))
MIKE = int(getenv('MIKE'))
PREVIEWS = join(__file__[:-6], '_previews')


class GaussBot(discord.Client):
    """The almighty gauss bot"""

    async def on_ready(self):
        """Searches for the bot connections on start"""
        guild = discord.utils.get(self.guilds, name=GUILD)
        print('{} is connected to {}'.format(self.user, guild.name))

    async def on_message(self, message):
        """
        Responding to messages

        Args:
            message(str): The content of the message.

        Returns:
            None.
        """
        if message.author == self.user:
            return
        if message.channel.name != "gauss":
            return
        if message.author.id == KENO and 'moin' in message.content.lower():
            await message.channel.send("Hallo, mein Meister")

        if message.author.id == MIKE and 'moin' in message.content.lower():
            await message.channel.send("Oh, it's Euler! Our battle will be legendary!")

        with open('discord_IDs.txt', 'a') as f:
            f.write("{}:{}\n".format(message.author.name, message.author.id))

        if message.content.lower() in ['rip', 'r.i.p.']:
            await message.channel.send('F')

        if message.content == 'Hi':
            response = 'Hi'
            await message.channel.send(response)

        elif 'integrate' in message.content:
            solved, integral, integrand, limits = do_integration(message.content)

            if not solved:
                await message.channel.send(integral)
                response = await self.wait_for('message')
                do_integration_again(integrand, response.content, limits)

            await message.channel.send('This is how I understood your query:')
            await message.channel.send(file=discord.File(join(PREVIEWS, 'input.png')))
            await message.channel.send('This is my solution:')
            await message.channel.send(file=discord.File(join(PREVIEWS, 'output.png')))

        elif 'diff' in message.content:
            solved, derivative = do_derivation(message.content)

            if not solved:
                pass
