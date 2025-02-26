from getpass import getpass

from kortical.helpers import is_interactive
from kortical.cloud import _random_seed
from kortical.cli._cmd_registry import command
from kortical.config import kortical_config
from kortical.secret import secret

from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_info, print_success, print_question
from kortical.helpers.encryption_helpers import decrypt


def _verify_password():
    credentials = decrypt(kortical_config.get("credentials"), key=_random_seed)
    print_question("Password:")
    password = getpass(prompt='') if is_interactive() == 'true' else input()

    if password != credentials['password']:
        raise KorticalKnownException(f"Incorrect password for email [{credentials['email']}].")
    return


@command('secret')
def command_secret(args):
    """
Allows you to securely store key-value pairs at a system level, accessible to all apps.

usage:
    kortical secret [-h]
    kortical secret set <key> <value> [--overwrite]
    kortical secret get <key>
    kortical secret delete <key>

options:
    -h, --help           Display help.
    <key>                Name of the secret you want to view.
    <value>              Contents of the secret.
    --overwrite          If storing a secret which has the same key as an existing secret, the old data is overwritten.


commands:
    set                  Set a new secret. You will be prompted for your password.
    get                  Retrieve the contents of a secret. You will be prompted for your password.
    delete               Delete an existing secret. You will be prompted for your password.

    """

    if args['set']:
        _verify_password()
        print_info("Verified! Setting secret...")

        # Set the secret
        secret.set(args['<key>'], args['<value>'], args['--overwrite'])
        print_success("Secret successfully stored.")

    elif args['get']:
        _verify_password()
        print_info("Verified! Getting secret...")

        # Get the secret
        value = secret.get(args['<key>'])
        print_success("Secret: ")
        print(f"\t{args['<key>']} = {value}")

    if args['delete']:
        _verify_password()
        print_info("Verified! Deleting secret...")

        # Delete the secret
        secret.delete(args['<key>'])
        print_success("Secret successfully deleted.")
