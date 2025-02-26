"""
Kortical Software Development Kit

usage:
    kortical <command> [<args>...] [-hv]

options:
    -h, --help     Display help.
    -v, --version  Display version.

Commands:
    config        Configures the Kortical SDK with your system URL and email/password credentials.
    status        View high level information about projects, environments + components.
    project       Manage projects.
    environment   Manage environments within a selected project.
    component     Manage components within a selected environment.
    model         Manage models that have been created on Kortical.
    app           Manage apps that have been deployed to Kortical, or exist locally.
    cronjob       Manage cronjobs (i.e automate regularly occurring tasks).
    docker        Manage Docker images, which are required for deploying apps.
    secret        Manage secrets (key-value pairs that are accessible across Kortical).
    storage       Manage Cloud storage.
    worker        Manage worker groups (i.e computers/hardware).
    usage         Manage usage information.

For more information on a command, run `kortical <cmd> --help`.
"""

import logging
import os
import sys
import warnings

from docopt import docopt
from docopt import DocoptExit

warnings.filterwarnings('ignore')

from . import _cmd_registry

# If you add a module containing commands, you must import it here for
# it to have any effect. Include the "# NOQA" comment to prevent
# flake8 warning about the unused import.
from . import _config       # NOQA
from . import _project      # N0QA
from . import _environment  # N0QA
from . import _component    # NOQA
from . import _model        # NOQA
from . import _app          # NOQA
from . import _cronjob      # NOQA
from . import _docker       # NOQA
from . import _status       # NOQA
from . import _storage      # NOQA
from . import _secret       # NOQA
from . import _worker       # NOQA
from . import _usage        # NOQA

from kortical import api
from kortical.config import kortical_config


def disable_logging():
    logging.disable(logging.DEBUG)
    logging.disable(logging.INFO)
    logging.disable(logging.WARNING)
    logging.disable(logging.ERROR)
    logging.disable(logging.CRITICAL)


def get_version():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, "../VERSION")) as f:
        return f.read().strip()


def handle_args(args):
    cmd = _cmd_registry.get_command(args['<command>'])
    if cmd is None:
        print(f"kortical: Unrecognised command [{args['<command>']}]", file=sys.stderr)
        raise DocoptExit()

    # Authentication required before using the CLI (i.e set up kortical config)
    if args['<command>'] != 'config':
        api.init()

    return cmd()


def map_aliases_on_sys_args():
    arg_aliases = [{
            'environment': ['e', 'env', 'environments', 'environmnet', 'envionment', 'enviromnet', 'enviroment'],
            'project': ['p', 'projects', 'proj', 'prj'],
            'app': ['a', 'apps'],
            'cronjob': ['cron'],
            'component': ['c', 'components', 'compoenent', 'cpt'],
            'model': ['m', 'models', 'modle', 'mdl'],
            'worker': ['w', 'workers'],
            'config': ['cfg'],
            'status': ['s']
        },
        {
            'challenger': ['ch', 'challengers', 'chal', 'chall'],
            'versions': ['v', 'vrs', 'version'],
            'config': ['cfg'],
            'kortical-config': ['kc'],
            'credentials': ['creds', 'cred', 'credential'],
            'list': ['l', 'ls'],
            'wait-for-components': ['wfc']
        },
        {
            'config': ['cfg'],
            'list': ['l', 'ls']
        }]

    for i in range(len(arg_aliases)):
        if i+1 < len(sys.argv):
            for correct, incorrect_list in arg_aliases[i].items():
                for incorrect in incorrect_list:
                    if sys.argv[i+1] == incorrect:
                        sys.argv[i+1] = correct


def main():
    kortical_config.use_memory_config = False
    warnings.filterwarnings('ignore')
    disable_logging()

    map_aliases_on_sys_args()

    args = docopt(__doc__, version=get_version(), options_first=True)

    return handle_args(args)


if __name__ == '__main__':
    main()
