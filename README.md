# <img align="left" width="100" src="https://upload.wikimedia.org/wikipedia/commons/9/9b/Carl_Friedrich_Gauss.jpg"> 
# &nbsp;&nbsp;&nbsp;Gauss Discord Bot
<br/>
<br/>
Johann Carl Friedrich Gauss  (30 April 1777 – 23 February 1855)
was a German mathematician and physicist who made significant
contributions to many fields in mathematics and science 
(taken from <a href="https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss">wikipedia</a>).

The gauss discord bot was initially designed to help with mathematical
inquiries of all sorts but is evolving into a meme machine.

## Requirements

This package requires python 3.6 as well as the external packages 
sympy and discord.

## Installation

There is currently no pip install option. The package may be installed by
copying and pasting the source code in your python directory.

## Usage

### User

The bot may be invoked by typing a message starting with 'gauss' followed by
the function you want to use. For an overview of the functions type 'gauss help'

### Host

To host the bot you need to install the package and be in possession of the
required .env file with the token for the bot. You can then run the bot by
executing a script with the following code:
```python
from gauss.bot import GaussBot, TOKEN


if __name__ == '__main__':
    client = GaussBot() 
    client.run(TOKEN) 
```

## Documentation

The documentation can be found at https://kenokrieger.github.io/gaussbot.

## Tests

Tests can be found in the tests/ directory. They are currently not set up
to be automatically executed with pytest.

## Contributing

Contributions are always welcome! To contribute fork the directory from
github and ask me for the bot token. For more detailed information see
'CONTRIBUTING.md'.

## License

This project is licensed under BSD-2-Clause License. For more information
see the LICENSE.txt file.
