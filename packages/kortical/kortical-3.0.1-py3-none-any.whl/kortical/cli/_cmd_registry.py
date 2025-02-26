from docopt import docopt
import sys
import traceback

from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_error, print_warning

_commands = {}


def command(name):
    def impl(fn):
        doc = fn.__doc__
        if name in _commands:
            raise RuntimeError(f"Multiple commands named [{name}].")

        def wrapper():
            try:
                args = docopt(doc)
                return fn(args)
            except KorticalKnownException as e:
                print_error(f'ERROR: {e}')
                sys.exit(1)
            except KeyboardInterrupt:
                print_warning("Terminating due to keyboard interrupt.")
            except Exception as e:
                print_error(f'ERROR: Operation failed due to unexpected error. {traceback.format_exc()}')
                sys.exit(1)

        _commands[name] = wrapper
    return impl


def get_command(name):
    if name not in _commands:
        return None
    return _commands[name]
