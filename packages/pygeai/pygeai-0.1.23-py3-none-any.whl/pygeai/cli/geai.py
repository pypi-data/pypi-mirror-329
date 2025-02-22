import sys

from pygeai.cli.commands.base import base_commands, base_options
from pygeai.cli.commands import ArgumentsEnum, Command
from pygeai.cli.parsers import CommandParser
from pygeai.cli.texts.help import CLI_USAGE
from pygeai.core.base.session import get_session
from pygeai.core.common.exceptions import UnknownArgumentError, MissingRequirementException, WrongArgumentError


def main():
    driver = CLIDriver()
    return driver.main()


class CLIDriver:

    def __init__(self, session=None):
        """
        Sets session to be used while running the command, either with a specified alias,
        environment variables or function parameters.
        Once the session is defined, it won't change during the curse of the execution.
        """
        arguments = sys.argv
        if "-a" in arguments or "--alias" in arguments:
            alias = self._get_alias(arguments)
            session = get_session(alias)

        self.session = get_session() if session is None else session

    def _get_alias(self, arguments: list):
        """
        Retrieves and removes alias and alias flag from argument list
        """
        alias_index = None

        if "-a" in arguments:
            alias_index = arguments.index("-a")
        elif "--alias" in arguments:
            alias_index = arguments.index("--alias")

        _ = arguments.pop(alias_index)
        alias = arguments.pop(alias_index)
        return alias

    def main(self, args=None):
        """
        If not argument is received, it defaults to help (first command in base_command list).
        Otherwise, it parses the arguments received to identify the appropriate command and either
        execute it or parse it again to detect subcommands.
        """
        try:
            if len(sys.argv) > 1:
                arg = sys.argv[1] if args is None else args[1]
                arguments = sys.argv[2:] if args is None else args[2:]

                command = CommandParser(base_commands, base_options).identify_command(arg)
            else:
                command = base_commands[0]
                arguments = []

            self.process_command(command, arguments)
        except (UnknownArgumentError, WrongArgumentError) as e:
            sys.stderr.write(f"usage: {CLI_USAGE}")
            sys.stderr.write(str(e))
            sys.stderr.write("\n")
        except MissingRequirementException as e:
            sys.stderr.write(f"ERROR: Something is missing! {e}")
        except KeyboardInterrupt:
            sys.stdout.write("\n")
        except Exception as e:
            sys.stderr.write(f"Unexpected error. Please report this bug to the developers. Error: {e}")
            return 255

    def process_command(self, command: Command, arguments: list[str]):
        """
        If the command has no action associated with it, it means it has subcommands, so it must be parsed again
        to identify it.
        """
        if command.action:
            if command.additional_args == ArgumentsEnum.NOT_AVAILABLE:
                command.action()
            else:
                option_list = CommandParser(base_commands, command.options).extract_option_list(arguments)
                command.action(option_list)
        elif command.subcommands:
            subcommand_arg = arguments[0] if len(arguments) > 0 else None
            subcommand_arguments = arguments[1:] if len(arguments) > 1 else []

            available_commands = command.subcommands
            available_options = command.options
            parser = CommandParser(available_commands, available_options)

            if not subcommand_arg:
                subcommand = command.subcommands[0]
            else:
                subcommand = parser.identify_command(subcommand_arg)

            if subcommand.additional_args == ArgumentsEnum.NOT_AVAILABLE:
                subcommand.action()
            else:
                option_list = CommandParser(None, subcommand.options).extract_option_list(subcommand_arguments)
                subcommand.action(option_list)

