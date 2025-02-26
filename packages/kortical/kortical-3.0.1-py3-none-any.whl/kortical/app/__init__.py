import os
from pathlib import Path

from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.api.app_instance import AppInstance
from kortical.cloud.cloud import IS_KUBERNETES_ENVIRONMENT
from kortical.helpers import format_config
from kortical.helpers.exceptions import KorticalKnownException


def is_running_in_cloud():
    return IS_KUBERNETES_ENVIRONMENT


def get_app_url():
    if is_running_in_cloud():
        return os.environ['KORE_APP_URL']
    else:
        return '/'


def get_app_config(format=None):

    if is_running_in_cloud():
        # Get config from platform
        project = Project.get_selected_project()
        environment = Environment.get_selected_environment(project)
        app = AppInstance.get_app_instance(project, environment, os.environ["KORE_COMPONENT_INSTANCE_ID"])
        config = app.get_app_config(format=format)
        return config

    # Search locally for a parent folder that has either an app_config or a config/app_config
    current_directory = os.getcwd()
    while True:
        # Get files, must be called "app_config" (ignore extension)
        app_config_files = [os.path.join(current_directory, f) for f in os.listdir(current_directory)
                            if os.path.isfile(os.path.join(current_directory, f)) and Path(f).stem == 'app_config']
        config_directory = os.path.join(current_directory, 'config')
        if os.path.exists(config_directory):
            app_config_files += [os.path.join(config_directory, f) for f in os.listdir(config_directory)
                                 if os.path.isfile(os.path.join(config_directory, f)) and Path(f).stem == 'app_config']

        # Read file
        for file in app_config_files:
            with open(file, 'r') as f:
                config = f.read()
                return format_config(config, format)

        # Recurse backwards
        path = Path(current_directory)
        current_directory = str(path.parent.absolute())
        if path.root == current_directory:
            raise KorticalKnownException(f"No app config found in directory [{os.getcwd()}]")


def get_version():

    if is_running_in_cloud():
        # Get version name from environment variable
        return f'v{os.environ["KORE_COMPONENT_VERSION"]}'
    else:
        # Locally, the app has no version. Versions are only created when the app is deployed.
        return None
