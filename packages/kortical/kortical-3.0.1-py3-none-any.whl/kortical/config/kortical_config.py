import os
import urllib.request
from datetime import datetime
from getpass import getpass
from pathlib import Path
import re
import yaml

import ssl
import certifi

from kortical import api
from kortical.helpers import is_interactive
from kortical.cloud import _random_seed
from kortical.cloud.cloud import IS_KUBERNETES_ENVIRONMENT

from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_info, print_success, print_error, print_question
from kortical.helpers.encryption_helpers import encrypt


use_memory_config = True
in_memory_config = {}


def in_home_dir():
    return os.getcwd() == str(Path.home())


def get_kortical_dir_name():
    return '.kortical'


def get_global_kortical_dir():
    global_kortical_dir = os.path.join(str(Path.home()), get_kortical_dir_name())
    if not os.path.exists(global_kortical_dir):
        os.mkdir(global_kortical_dir)
    return global_kortical_dir


def get_local_kortical_dirs():
    # Returns a list of .kortical folder paths that apply to the cwd.
    paths = []

    current_path = os.getcwd()
    parent_path = os.path.abspath(os.path.join(current_path, os.pardir))

    while True:

        # If at root or home directory
        if os.path.dirname(current_path) == current_path or current_path == str(Path.home()):
            paths.reverse()
            return paths

        # Search child directories of current level
        if get_kortical_dir_name() in next(os.walk(current_path))[1]:
            local_kortical_dir = os.path.join(current_path, get_kortical_dir_name())
            paths.append(local_kortical_dir)

        # Recurse up the tree
        current_path = parent_path
        parent_path = os.path.abspath(os.path.join(current_path, os.pardir))


def get_active_directory():
    local_kortical_folders = get_local_kortical_dirs()
    if len(local_kortical_folders) > 1:
        return local_kortical_folders[-1]
    else:
        return get_global_kortical_dir()

# Interactive user prompts and validation functions for entering details through the terminal

def user_prompt_url():
    print_question(f"Please enter your system URL here:")
    url = input()
    url = clean_url(url)

    if _valid_url(url):
        return url
    else:
        return user_prompt_url()


def clean_url(url):
    if url is None:
        return url

    if url.startswith('https://'):
        url = url[len('https://'):]
    url = 'https://' + '/'.join(re.split('/|#', url)[:3])

    return url


def user_prompt_credentials(url=None):
    print_question(f"Please enter kortical login email:")
    email = input()
    print_question("Password:")
    password = getpass(prompt='') if is_interactive() == 'true' else input()
    credentials = {'email': email, 'password': password}
    encrypted_credentials = encrypt(credentials, key=_random_seed)

    if _valid_credentials(encrypted_credentials, url):
        return encrypted_credentials
    else:
        return user_prompt_credentials()


def _valid_url(url):
    try:
        urllib.request.urlopen(url)
        return True
    except:
        try:
            cafile = certifi.where()
            context = ssl.create_default_context(cafile=cafile)
            urllib.request.urlopen(url, context=context)
            return True
        except:
            print_error(f"Invalid System URL = [{url}]!\n"
                        "Ensure the format is https://platform.kortical.com/<company>/<system> "
                        "and that the link is registered to an existing system.\n")
            return False


def _valid_credentials(encrypted_credentials, url=None):
    if url is None:
        url = get('system_url')
    try:
        api.init(url, encrypted_credentials)
        return True
    except:
        print_error(f"Invalid credentials for system URL {url}\n")
        return False


def _valid_datetime_str(x):
    try:
        datetime.fromisoformat(x)
        return True
    except ValueError:
        print_error("Incorrect format for datetime string, should be dd/mm/yyyy, hh:mm:ss")
        return False


def _is_valid_id(id_):
    if id_ is not None and not str(id_).isdecimal():
        print_error(f"id must be a number, not [{id_}]\n")
        return False
    return True


# TODO P&E I don't see prompt used anywhere. Selected project id should be a hidden property, I think we added some of these so I'll just do a simple add for now and hope some mechanism appears in a merge
# Kortical config data definition
CONFIG_DEFINITION = {
    'system_url':
        {'prompt': user_prompt_url, 'validation': _valid_url},
    'credentials':
        {'prompt': user_prompt_credentials, 'validation': _valid_credentials},
    'selected_project_id':
        {'validation': _is_valid_id},
    'selected_environment_id':
        {'validation': _is_valid_id},
    'time_of_last_api_call':
        {'validation': _valid_datetime_str},
}


# Get config details at global/local level
def _read_from_folder(path):
    config = {}
    config_path = os.path.join(path, 'config.yml')

    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)

    return config


def _write_to_folder(path, key, value, print=False):
    config_path = os.path.join(path, 'config.yml')
    if not os.path.exists(config_path):
        with open(config_path, 'w') as f:
            yaml.safe_dump({}, f)
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
        if key in config:
            message1 = f"Config overwritten at [{config_path}]:"
            message2 = f"{key}: {config[key]} \n" \
                       f"\t--> {value}"
        else:
            message1 = f"Config set at [{config_path}]:"
            message2 = f"{key}: {value}"
        config.update({key: value})
    with open(config_path, 'w') as f:
        yaml.safe_dump(config, f)
        if print:
            print_success(message1)
            print_info(message2)


def _unset(path, key):
    config_path = os.path.join(path, 'config.yml')
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            if config is None:
                config = {}
            config.pop(key, '')
        with open(config_path, 'w') as f:
            yaml.safe_dump(config, f)


def _set_in_memory(key, value):
    global in_memory_config
    in_memory_config[key] = value


def init():
    global in_memory_config
    if use_memory_config:
        in_memory_config = {}
        return in_memory_config

    config_dir = os.path.join(os.getcwd(), get_kortical_dir_name())

    if os.path.exists(config_dir):
        raise KorticalKnownException(f"There is an existing config folder at [{config_dir}].")
    else:
        os.mkdir(config_dir)
        print_success(f"New config folder created at [{config_dir}].")


def get(key=None, force_global=False):
    global in_memory_config

    # Read from kubernetes
    if IS_KUBERNETES_ENVIRONMENT:
        # This is the internal UI statefulsets DNS
        # It is not currently possible to get the namespace when loading the in-cluster kubernetes config
        # using the Python client. But we can directly read the secret kubernetes generated when creating the pod.
        with open('/var/run/secrets/kubernetes.io/serviceaccount/namespace', 'r') as file:
            namespace = file.read()
        url = f'http://ingress.{namespace}.svc.cluster.local'
        email = os.environ['SERVICE_ACCOUNT_EMAIL']
        password = os.environ.get('SERVICE_ACCOUNT_SECRET')
        if password is None:
            password = os.environ.get('SERVICE_ACCOUNT_PASSWORD')
            if password is None:
                raise Exception('Credentials for Kortical were not found.')
        encrypted_credentials = encrypt({'email': email, 'password': password}, key=_random_seed)

        config = {'system_url': url, 'credentials': encrypted_credentials}

    # Read directly from config files (CLI)
    else:
        config = _read_from_folder(path=get_global_kortical_dir())
        if not force_global:
            for dir in get_local_kortical_dirs():
                local_config = _read_from_folder(dir)
                config.update(local_config)

    # Use in-memory config, this works like a "local" .kortical folder for the current process (SDK)
    if use_memory_config:
        config.update(in_memory_config)

    return config.get(key) if key else config


def set(key, value, force_global=False, print=True):
    global in_memory_config

    # Validation
    if key not in CONFIG_DEFINITION:
        raise KorticalKnownException(f"Invalid key [{key}]. Choose from following: {list(CONFIG_DEFINITION.keys())}")
    if not CONFIG_DEFINITION[key]['validation'](value):
        raise KorticalKnownException(f"Invalid value [{key} = {value}]")

    # Update in-memory config (SDK)
    if use_memory_config:

        # Write to in-memory config (which behaves like a local .kortical folder)
        if not force_global:
            _set_in_memory(key, value)
            if print:
                print_success(f"Config set in memory, {key}: {in_memory_config[key]}")

        # Write to global .kortical folder, and unset any other occurrences along the current path
        else:
            _write_to_folder(get_global_kortical_dir(), key, value, print)
            for path in get_local_kortical_dirs():
                _unset(path, key)
            in_memory_config.pop(key, None)

    # Update config files (CLI)
    else:

        # Write to local-most .kortical folder
        if not force_global and len(get_local_kortical_dirs()) > 0:
            _write_to_folder(get_local_kortical_dirs()[-1], key, value, print)

        # Write to global .kortical folder, and unset any other occurrences along the current path
        else:
            _write_to_folder(get_global_kortical_dir(), key, value, print)
            for path in get_local_kortical_dirs():
                _unset(path, key)
