# <img align="left" width="100" src="https://upload.wikimedia.org/wikipedia/commons/9/9b/Carl_Friedrich_Gauss.jpg"> 
# &nbsp;&nbsp;&nbsp;Gauss Discord Bot
<br/>
<br/>
Johann Carl Friedrich Gauss  (30 April 1777 – 23 February 1855)
was a German mathematician and physicist who made significant
contributions to many fields in mathematics and science 
(taken from <a href="https://en.wikipedia.org/wiki/Carl_Friedrich_Gauss">wikipedia</a>).

The gauss discord bot is designed to help with mathematical
inquiries of all sorts. He will help you to solve integrals and 
to differentiate and probably even more in the future.

## Requirements

This package requires python 3.6 or higher aswell as the external packages 
sympy and discord.

## Installation

There is currently no pip install option. The package may be installed by
copy pasting the source code in your python directory.

## Usage

### User

#### Integration
To integrate an expression, simply start of with 'integrate' followed by 
the expression to integrate. You may also specify the integration
variable *x* by 

- specifying it with a d*x*

- writing '*, x*' at the end of the integrand

- or saying 'with respect to *x*'

You can also specify the limits by including *from* *to* after the integrand.

To list some examples:
```
integrate sin(x) du
integrate cos(u) from 0 to pi
integrate a**2 + b^2 - c, c
integrate ax + b, x from 0 to b
integrate exp(-r^2) from -pi to pi
```
### Host

To host the bot you need to install the package and be in possesion of the
required .env file with the token for the bot. You can then run the bot by
executing a script with the following code:
```python
from gauss.bot import GaussBot, TOKEN


if __name__ == '__main__':
    client = GaussBot()
    client.run(TOKEN)
```

## Documentation

All funtions and modules are documented in the code directly. In the
near future I will set up sphinx to build a documentation automatically.

## Tests

Tests can be found in the tests/ directory. They are currently not set up
to be automatically executed with pytest.

## Contributing

Contributions are always welcome! To contribute fork the directory from
github and ask me for the bot token. You may then develop your feature
and issue a pull request. Don't forget the unit tests :)

## License

This project is licensed under BSD-2-Clause License. For more information
see the LICENSE.txt file.


