"""Main execution script"""

from gauss.bot import GaussBot, TOKEN


if __name__ == '__main__':
    client = GaussBot()
    client.run(TOKEN)
