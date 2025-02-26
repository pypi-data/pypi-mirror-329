from kortical.api.project import Project
from kortical.cli._cmd_registry import command
from kortical.cli.helpers.environment_helpers import display_list_environments, display_selected_environment
from kortical.cli.helpers.kortical_config_helpers import display_kortical_config_list

from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_success, print_question, print_title, print_error, format_question, display_list, print_warning, user_prompt_yes_no, user_prompt_option, print_options


def display_list_projects():
    projects = Project.list(include_created_by=True)
    print_title("Projects:")
    display_list(projects)


def display_selected_project(project, is_success=False):
    if is_success:
        print_ = print_success
    else:
        print_ = print_title
    print_(f"Project [{project.name}] selected.")
    display_list(project)


def user_prompt_create_environments():
    print_options("Would you like to:",
                  {'1': 'Use the default environments: Integration, UAT, Production',
                   '2': 'Enter a custom set of environments'})
    response = user_prompt_option("Please enter '1' or '2'.", options=['1', '2'])

    if response == '1':
        comma_separated_environment_names = None
        return comma_separated_environment_names
    elif response == '2':
        print_question("\nPlease enter a list in the format 'environment_1,environment_2,environment_n', making sure they are ordered correctly."
                       "\nThe least production environment being on the left and the most production on the right.")
        comma_separated_environment_names = input()
        return comma_separated_environment_names
    else:
        print_error("Invalid input.")
        user_prompt_create_environments()


def display_and_select_first_environment(project):
    # It's an ordered list so zero is the lowest
    environments = project.list_environments()
    display_list_environments(project)
    environment = environments[0]
    environment.select()
    display_selected_environment(environment, True)


@command('project')
def command_project(args):
    """
Controls creation and management of projects on Kortical.

Definitions:

Project             A framework for the deployment and management of apps + models on Kortical. Projects are
                    comprised of multiple environments, and environments may contain several components.
Kortical Config     This allows you to configure settings (i.e worker group, replicas) at
                    the project/environment/component level.

usage:
    kortical project [-h]
    kortical project list
    kortical project create <project-name> [--environments=<environment-names>]
    kortical project select <project-name-or-id>
    kortical project deselect
    kortical project delete [-f] [<project-name-or-id>]
    kortical project kortical-config get
    kortical project kortical-config set <key> <value>
    kortical project kortical-config inherit <key>


options:
    -h, --help              Display help.
    -f, --force             Execute command without confirmation.
    <project-name-or-id>    Name or ID used to refer to a project; run [kortical project list] to view this.
    <environment-names>     Comma-separated list of environments you want to create.


commands:
    list                  Returns a list of your Kortical projects.
    create                Creates a new project with the specified name.
    select                Selects a project (required for managing environments and apps).
    deselect              Deselects the current project.
    delete                Deletes a project.
    kortical-config       Adjust Kortical config at the project level.


aliases:
    project             p proj projects
    kortical-config     kc
    """

    if args['list']:
        display_list_projects()

    elif args['create']:
        comma_separated_environment_names = args['--environments'] if args['--environments'] else user_prompt_create_environments()
        project = Project.create_project(args['<project-name>'], comma_separated_environment_names)
        print_success("Project created successfully!")
        display_list(project)
        project.select()
        print_success(f"Project [{project.name}] selected.")
        display_and_select_first_environment(project)

    elif args['select']:
        project_name_or_id = args['<project-name-or-id>']
        project = Project.get_project(project_name_or_id)
        if project is None:
            raise KorticalKnownException(f"Project [{project_name_or_id}] does not exist.")
        project.select()
        display_selected_project(project, True)
        display_and_select_first_environment(project)

    elif args['deselect']:
        Project.deselect_project()
        print_success("No selected project.")

    elif args['delete']:
        project_name_or_id = args.get('<project-name-or-id>')
        if project_name_or_id is None:
            project = Project.get_selected_project()
        else:
            project = Project.get_project(project_name_or_id)
        if project is None:
            print_error(f"Could not delete project [{project_name_or_id}], it does not exist.")
            return

        if not args['--force']:
            display_list_projects()
            print_warning(f"WARNING: The project [{project.name}] and its associated environments/components will all be deleted.")

            should_delete = user_prompt_yes_no(f"Are you sure you want to continue? [y/N]\n")
            if not should_delete:
                print_error("Project delete cancelled.")
                return

        project.delete()
        print_success(f"Project [{project.name}] deleted.")

    if args['kortical-config']:
        project = Project.get_selected_project()

        if args['get']:
            display_selected_project(project)
            display_kortical_config_list(project)

        if args['set']:
            kortical_config = {args['<key>']: args['<value>']}
            project.set_kortical_config(kortical_config)
            display_selected_project(project)
            display_kortical_config_list(project)

        if args['inherit']:
            kortical_config = {args['<key>']: None}
            project.set_kortical_config(kortical_config)
            display_selected_project(project)
            display_kortical_config_list(project)
