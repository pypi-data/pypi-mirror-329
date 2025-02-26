from kortical.api.environment import Environment
from kortical.helpers.print_helpers import print_info, print_success, print_title, display_list


def display_list_environments(project):
    environments = Environment.list(project, include_created_by=True)
    print_title(f"Environments in project [{project.name}]:")
    display_list(environments)
    return environments


def display_list_challenger_environments(project, environment, challenger_environments=None):
    print_title(f"Challenger environments for environment [{environment.name}] in project [{project.name}]:")
    display_list(challenger_environments)


def display_selected_environment(environment, is_success=False):
    if is_success:
        print_ = print_success
    else:
        print_ = print_title
    print_(f"Environment [{environment.name}] selected.")
    display_list(environment)