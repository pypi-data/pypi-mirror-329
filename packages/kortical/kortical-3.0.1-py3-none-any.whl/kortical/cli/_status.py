import os

from kortical.api.app import get_local_apps
from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.cli._cmd_registry import command
from kortical.cli._project import display_selected_project
from kortical.cli._environment import display_selected_environment
from kortical.cli.helpers import get_user_email
from kortical.cli.helpers.component_helpers import display_list_component_instances, display_list_component_instances_urls
from kortical.config import kortical_config
from kortical.helpers.print_helpers import print_title, print_warning, print_info


@command('status')
def command_status(args):
    """
Returns a high-level summary of your credentials and selected project/environment/components.

usage:
    kortical status [-h]

options:
    -h, --help            Display help.


aliases:
    status           s
    """

    config_active_directory = kortical_config.get_active_directory()
    url = kortical_config.get('system_url')
    email = get_user_email()
    print_title(f"Active config directory [{config_active_directory}]")
    print_title(f"System url [{url}]")
    print_title(f"User credentials [{email}]")
    project = Project.get_selected_project(throw=False)
    if project is None:
        print_title("No selected project")
    else:
        display_selected_project(project)

        environment = Environment.get_selected_environment(project, throw=False)

        if environment is None:
            print_title("No selected environment")
        else:
            display_selected_environment(environment)

            component_instances = display_list_component_instances(project, environment)
            display_list_component_instances_urls(component_instances, project, environment)

    app_directory = os.getcwd()
    local_app_names = list(get_local_apps(app_directory).keys())

    if len(local_app_names) == 0:
        print_warning(f"No apps found, are you sure you're in the app directory?\n"
                      f"{os.getcwd()}")
    print_title(f"Apps in current directory [{os.getcwd()}]")
    for app_name in local_app_names:
        print_info(app_name)
