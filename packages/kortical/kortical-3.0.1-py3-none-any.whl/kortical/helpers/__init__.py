import json
import os

import yaml

from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_question, print_warning


def is_interactive():

    if os.isatty(0) or ("PYCHARM_HOSTED" in os.environ and 'KORTICAL_TEST' not in os.environ):
        return 'true'
    # this condition is nearly always false, except for CI builds
    elif "CI_INTERACTIVE_TESTS" in os.environ:
        return 'non_interactive_ci'
    else:
        return 'false'


def load_from_path(file_path, throw=True):
    file_path = os.path.abspath(file_path)

    try:
        with open(file_path) as f:
            text = f.read()
        return text
    except:
        if throw:
            raise KorticalKnownException(f"Path [{file_path}] was not found.")
        else:
            print_warning(f"Path [{file_path}] was not found.")
            return None


def check_project_and_environment_selected():
    from kortical.api.project import Project
    from kortical.api.environment import Environment

    project = Project.get_selected_project()
    environment = Environment.get_selected_environment(project)

    return project, environment


def format_config(config, format):
    try:
        if format == 'json':
            return json.loads(config)
        elif format == 'yaml' or format == 'yml':
            return yaml.safe_load(config)
        else:
            return config
    except:
        raise KorticalKnownException(f"Failed to load config in format [{format}].\n\n"
                                     f"Config: {config}")


def str2enum(input, enum):
    if input is None:
        return None

    # Accept str or enum, return enum
    enum_options = list(enum.__members__.values())
    str_options = [e.value for e in enum]

    if isinstance(input, enum) and input in enum_options:
        return input
    elif isinstance(input, str) and input in str_options:
        return next(e for e in enum if e.value == input)
    else:
        raise KorticalKnownException(f"Expected {enum_options} or {str_options}, received [{input}].")
