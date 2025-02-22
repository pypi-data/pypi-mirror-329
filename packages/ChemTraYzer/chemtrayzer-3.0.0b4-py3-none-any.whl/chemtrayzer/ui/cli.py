"""Main command line interface

To add a new command to the chemtrayzer command, add it to the _COMMANDS
dictionary. The key is the name of the command and the value is either a
CommandLineInterface class or a function that is called with the parsed
arguments.
"""
import sys
from abc import ABC, abstractmethod
from argparse import ArgumentParser, Namespace

from chemtrayzer.engine.cmdtools import CommandLineInterface
from chemtrayzer.ui.rxn_sampling import AnalyzeTrajCLI, RunMDCLI


# to enable the test command, we need to ensure that pytest is installed
try:
    import pytest   # noqa
except ImportError:
    _pytest = False
else:
    _pytest = True
    from chemtrayzer.engine.testing import BatchCLI

class Command(ABC):
    """Abstract base class for commands"""

    @abstractmethod
    def __call__(self, args: Namespace, argv: list[str]):
        """
        :param args: parsed known arguments
        :param argv: all argument values
        """


class CliCommand(Command):
    """Command that simply wraps a CommandLineInterface"""

    def __init__(self, name: str, cli_type: type[CommandLineInterface]):
        self.name = name
        self.cli_type = cli_type

    def __call__(self, args: Namespace, argv: list[str]):
        cli = self.cli_type(
                    script=__file__,
                    prog=f'{argv[0]} {self.name}'
                )
        # Each CLI object has its own parser which is not a subparser -> remove
        # the first argument and just keep the command
        cli.start(argv[1:])


# The chemtrayzer command can be called with subcommands like this:
# `chemtrayzer test`. Here test is a subcommand of chemtrayzer.
# Each subcommand has its own parser, function and name. The name and function
# have to be registered here while the parser will be created automatically.
_COMMANDS: dict[str, Command] = {
    'analyze': CliCommand('analyze', AnalyzeTrajCLI),
    'runmd': CliCommand('runmd', RunMDCLI),
}

if _pytest:
    _COMMANDS['test'] = CliCommand('test', BatchCLI)

def main():
    '''main function that is called with the chemtrayzer command'''

    # set up basic parser
    parser = ArgumentParser()
    allowed_cmds_str = "'" + "', '".join(_COMMANDS.keys()) + "'"
    subparser_action = parser.add_subparsers(
        dest='__cmd__', # stores command name in __cmd__
        help=f'ChemTrayZer command (choose from {allowed_cmds_str}/LTT/chemt'
             'rayzer/tmp/24_11_08_tutorial).'
             ' Use "%(prog)s COMMAND -h" for help.',
        metavar='COMMAND',
        required=True
        )

    for name, _ in _COMMANDS.items():
        # do only partial parsing here -> no help and no abbrev allowed
        _ = subparser_action.add_parser(name,
                                        add_help=False,
                                        allow_abbrev=False)

    # parse arguments and execute the command
    args, _ = parser.parse_known_args()

    # very crude error handling b/c the commands should handle errors
    try:
        _COMMANDS[args.__cmd__](args, sys.argv)
    except Exception as e:
        parser.error(str(e))

if __name__ == '__main__':
    main()
