from os import getenv

import discord
from dotenv import load_dotenv

from gauss.brain import do_integration, do_integration_again

load_dotenv()
TOKEN: str = getenv('DISCORD_TOKEN')
GUILD: str = getenv('DISCORD_GUILD')


class gauss(discord.Client):
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

        if message.content == 'Hi':
            response: str = 'Hi'
            await message.channel.send(response)

        elif 'integrate' in message.content:
            solved, integral, integrand, limits = do_integration(message.content)

            if solved:
                await message.channel.send(integral)
            elif not solved:
                await message.channel.send(integral)
                response = await self.wait_for('message')
                integral = do_integration_again(integrand, response.content, limits)

                await message.channel.send(integral)
