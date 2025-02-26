from kortical.cloud import _random_seed
from kortical.cli._cmd_registry import command
from kortical.config import kortical_config
from kortical.helpers.print_helpers import print_info, format_question, print_success
from kortical.helpers.encryption_helpers import encrypt
from kortical.helpers.exceptions import KorticalKnownException


def _launch_prompts(args):

    if args['--quiet'] and args['--prompt-for-details']:
        raise KorticalKnownException("You cannot use --quiet and --prompt-for-details options at the same time.")
    elif not args['--quiet'] and args['--prompt-for-details']:
        return True
    elif args['--quiet'] and not args['--prompt-for-details']:
        return False
    # Default behaviour (no options)
    else:
        if kortical_config.get('system_url', force_global=True) is None:
            return True
        else:
            return False


@command('config')
def command_config(args):
    """
Initial setup, required before running any commands on Kortical CLI/SDK.

usage:
    kortical config [-h]
    kortical config init [-p] [-q]
    kortical config get [--global]
    kortical config set <key> <value> [--global]
    kortical config credentials to_string --email=<email> --password=<password>
    kortical config credentials from_string [-q] <credentials_string>

options:
    -h, --help                  Display help.
    -p, --prompt-for-details    Execute command with user prompts.
    -q, --quiet                 Execute command without user prompts.
    --global                    Use this to target the .kortical folder in your home folder.
    <email>                     Email used to login to the platform.
    <password>                  Password used to login to the platform.
    <credentials_string>        An encrypted string representing your email/password login details;
                                to obtain this, run [kortical config credentials to_string].


commands:
    init                        Creates an empty .kortical folder in your current working directory. If you want to initialise
                                local config different to your global settings, use --prompt-for-details.
    get                         View Kortical config files that are active from your current working directory. When config
                                is found in several files, the more local values takes precedence. Use --global
                                to only view config in your home folder.
    set                         Sets an item of config in your most local .kortical folder (unless you use --global)
    credentials                 Encrypt/stores your platform login details.


aliases:
    config              cfg
    credentials         creds credential
    """

    if args['init']:

        kortical_config.init()

        if _launch_prompts(args):

            # prompt for URL, save
            url = kortical_config.user_prompt_url()
            kortical_config.set('system_url', url)

            # Prompt for email/password, save
            encrypted_credentials = kortical_config.user_prompt_credentials()
            kortical_config.set('credentials', encrypted_credentials)

            if not kortical_config.in_home_dir() or kortical_config.get('system_url', force_global=True) is None:
                response = input(format_question(f"Save URL and credentials to global config? [y/N]\n"))
                if response.lower()[0] == 'y':
                    kortical_config.set('system_url', url, force_global=True)
                    kortical_config.set('credentials', encrypted_credentials, force_global=True)

    elif args['set']:
        # if user is passing in a url, clean it
        if args['<key>'] == 'system_url':
            args['<value>'] = kortical_config.clean_url(args['<value>'])

        # Set the key/value pair to config.yml
        is_global = True if args['--global'] else False
        kortical_config.set(args['<key>'], args['<value>'], force_global=is_global)
        return

    elif args['get']:

        is_global = True if args['--global'] else False

        # Get config folder paths
        config_file_paths = [kortical_config.get_global_kortical_dir()]
        if kortical_config.get_local_kortical_dirs() and not is_global:
            config_file_paths.extend(kortical_config.get_local_kortical_dirs())

        config = kortical_config.get(force_global=is_global)

        print_success(f"Config found at: {config_file_paths}\n")
        print_success("Kortical Config:")
        if type(config) == dict:
            for key, value in config.items():
                print_info(f"\t{key}: {value}")
        else:
            print_info(f"\t{args['--key']}: {config}")

    elif args['credentials']:

        # Converts an email/password pair to an encrypted b64 string
        if args['to_string']:
            encrypted_credentials = encrypt({'email': args['--email'], 'password': args['--password']}, key=_random_seed)
            print(encrypted_credentials)

        # Saves a b64 encoded string to local config.yml
        elif args['from_string']:
            # Put in .kortical folder
            kortical_config.set('credentials', args['<credentials_string>'])

            # Option to also set this as global
            if not args['--quiet']:
                response = input(format_question(f"Save these credentials to global config? [y/N]\n"))
                if response.lower()[0] == 'y':
                    kortical_config.set('credentials', args['<credentials_string>'], force_global=True)
