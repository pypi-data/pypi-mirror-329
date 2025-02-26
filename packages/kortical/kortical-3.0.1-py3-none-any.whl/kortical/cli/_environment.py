import os.path

from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.cli._cmd_registry import command
from kortical.cli._project import display_selected_project
from kortical.cli.helpers import get_user_email
from kortical.cli.helpers.component_helpers import display_list_component_instances, display_list_component_instances_urls
from kortical.cli.helpers.environment_helpers import display_list_environments, display_selected_environment, display_list_challenger_environments
from kortical.cli.helpers.kortical_config_helpers import display_kortical_config_list

from kortical.helpers import load_from_path, check_project_and_environment_selected
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_info, print_warning, print_error, print_success, print_title, user_prompt_yes_no, display_list


def non_challenger_environment_warning(environment, action):
    if not environment._is_challenger:
        print_warning(f"WARNING: You are about to {action} the [{environment.name}] environment!")
        should_continue = user_prompt_yes_no("Are you sure you want to continue? [y/N]\n")
        return should_continue


@command('environment')
def command_app(args):
    """
Controls creation and management of environments within a selected project on Kortical.

Definitions:

Environment           A collection of deployed apps + models on Kortical. Environments are chained together within a project,
                      where the contents of one environment are promoted to the next. The default list of environments
                      is Integration --> UAT --> Production.
Challenger            A new environment; this is usually cloned from one of the main environments e.g to implement bug
                      fixes for apps, or monitor the performance of an improved model.
Environment Config    External settings that may be used to alter the behaviour of an environment's components.
                      Environment config does not change during environment promotion.
Kortical Config       This allows you to configure settings (i.e worker group, replicas) at
                      the project/environment/component level.

usage:
    kortical environment [-h]
    kortical environment list [--all]
    kortical environment create <environment-name> [--promotes-to=<environment-name-or-id>] [--component-config=<file-path>]
    kortical environment select <environment-name-or-id>
    kortical environment config get
    kortical environment config set --config=<file-path>
    kortical environment delete [-f] [<environment-name-or-id>]
    kortical environment promote [-f]
    kortical environment challenger list [--user=<user_email_or_id>] [--all]
    kortical environment challenger create <challenger-environment-name> [--from=<environment-name-or-id>] [--component-config=<file-path>]
    kortical environment wait-for-components [--timeout=<timeout>]
    kortical environment kortical-config get
    kortical environment kortical-config set <key> <value>
    kortical environment kortical-config inherit <key>
    kortical environment component-config set --component-config=<file-path>



options:
    -h, --help                  Display help.
    -f, --force                 Execute command without confirmation.
    <environment-name-or-id>    Name or ID used to refer to an environment; run [kortical environment list] to view this.
    <timeout>                   Time to wait for app to reach a running state (in seconds).

commands:
    list                    Returns a list of environments within the selected Kortical project.
    create                  Creates an environment within the selected project.
    select                  Selects an environment (required for managing components).
    config                  Configures settings for the environment; this remains static
                            (i.e. it does not change when environments are promoted).
    delete                  Deletes an environment and its components.
    promote                 Promotes all of the components in the selected environment to the next environment.
    challenger              View/create challenger environments. By default, a challenger is cloned from the selected environment.
    wait-for-components     Wait for all component ins this environment to be running and ready to serve requests
    kortical-config         Adjust Kortical config at the environment level.
    component-config        Adjust the components (apps/models) that make up the environment, their versions, etc.


aliases:
    environment         e env environments
    challenger          ch challengers
    config              cfg
    challenger          ch chal challengers
    kortical-config     kc
    wait-for-components wfc
    """

    project = Project.get_selected_project()

    if args['list'] and not args['challenger']:
        display_selected_project(project)
        environments = display_list_environments(project)
        if args.get('--all'):
            for environment in environments:
                challenger_environments = environment.list_challengers()
                display_list_challenger_environments(project, environment, challenger_environments)

    elif args['create'] and not args['challenger']:
        environment_name = args.get('<environment-name>')
        if environment_name is None:
            raise KorticalKnownException("Please pass an <environment-name> to this command.")
        promotes_to_environment_name_or_id = args.get('--promotes-to')
        promotes_to_environment = None
        if promotes_to_environment_name_or_id is not None:
            promotes_to_environment = Environment.get_environment(project, promotes_to_environment_name_or_id)
            if promotes_to_environment.is_challenger():
                raise KorticalKnownException("Cannot create an environment promoting to a challenger environment.")
        component_config = None
        component_config_path = args.get('--component-config')
        if component_config_path is not None:
            if not os.path.isfile(component_config_path):
                raise KorticalKnownException(
                    f"Unable to find the component config path [{component_config_path}] from the folder [{os.getcwd()}]")
            with open(component_config_path) as f:
                component_config = f.read()
        environment = Environment.create_environment(
            project,
            environment_name,
            promotes_to_environment_name_or_id=promotes_to_environment.id,
            component_config=component_config
        )
        print_success(f"Environment [{environment.name}] created.")
        environment.select()
        display_selected_environment(environment, True)
        display_list_component_instances(project, environment)

    elif args['select']:
        environment_name_or_id = args.get('<environment-name-or-id>')
        environment = Environment.get_environment(project, environment_name_or_id)
        if environment is None:
            raise KorticalKnownException(f"Environment [{environment_name_or_id}] does not exist in project [{project.name}].")
        environment.select()
        display_selected_environment(environment, True)
        display_list_component_instances(project, environment)

    elif args['config']:
        _, environment = check_project_and_environment_selected()

        if args['get']:
            config = environment.get_environment_config()
            print_success(f"Environment config for project [{project.name}], environment [{environment.name}]:")
            print_info(str(config))

        if args['set']:
            environment_config = load_from_path(args['--config'])
            config = environment.set_environment_config(environment_config)
            print_success(f"Environment config set for project [{project.name}], environment [{environment.name}]:")
            print_info(str(config))

    elif args['delete']:
        environment_name_or_id = args.get('<environment-name-or-id>')
        if environment_name_or_id is None:
            environment = Environment.get_selected_environment(project)
        else:
            environment = Environment.get_environment(project, environment_name_or_id)
        if environment is None:
            print_error(f"Could not delete environment [{environment_name_or_id}], environment does not exist.")
            return

        if not args['--force']:
            if not environment._is_challenger:
                should_delete = non_challenger_environment_warning(environment, "delete")
            else:
                should_delete = user_prompt_yes_no(f"Environment [{environment.name}] will be deleted - Proceed? [y/N]\n")
            if not should_delete:
                print_error("Environment delete cancelled.")
                return

        response = environment.delete()
        if response['result'] == 'success':
            print_success(f"Environment [{environment.name}] deleted.")
        else:
            print_error(response.get('message'))
            if len(response['challengers']) != 0:
                print_title("Challengers blocking deletion:")
                for challenger in response['challengers']:
                    display_list(challenger)
            if response['depending'] is not None:
                print_title("Environment blocking deletion:")
                display_list(response['depending'])

    elif args['promote']:
        _, environment = check_project_and_environment_selected()
        next_environment = environment.get_promotes_to_environment()
        if next_environment is None:
            raise KorticalKnownException(f"Cannot promote environment [{environment.name}] "
                                         f"as there is no environment set to promote to.")

        print_title(f"From environment [{environment.name}].")
        display_list(environment)
        display_list_component_instances(project, environment)
        print_title(f"To environment [{next_environment.name}].")
        display_list(next_environment)
        display_list_component_instances(project, next_environment)

        if not args['--force']:
            if not environment._is_challenger:
                should_promote = non_challenger_environment_warning(environment, f"promote to [{next_environment.name}] from")
            else:
                should_promote = user_prompt_yes_no(f"Environment [{environment.name}] will be promoted "
                                                    f"to environment [{next_environment.name}] - Proceed? [y/N]\n")
            if not should_promote:
                print_error("Environment promote cancelled.")
                return

        environment.promote()
        print_success(f"Environment [{environment.name}] was promoted to [{next_environment.name}].")

        # Print new contents of next environment
        component_instances = display_list_component_instances(project, next_environment)
        display_list_component_instances_urls(component_instances, project, next_environment)

    elif args['challenger']:
        _, environment = check_project_and_environment_selected()

        if args['list']:
            if environment._is_challenger:
                environment = environment.get_promotes_to_environment()
            else:
                display_selected_environment(environment)
            if '--all' in args:
                challenger_environments = environment.list_challengers()
            else:
                email = get_user_email() if args['--user'] is None else args['--user']
                challenger_environments = environment.list_challengers(email)
            display_list_challenger_environments(project, environment, challenger_environments)

        elif args['create']:
            challenger_name = args.get('<challenger-environment-name>')
            if challenger_name is None:
                raise KorticalKnownException("Please pass a <challenger-environment-name> to this command.")
            from_environment_name_or_id = args.get('--from')
            if from_environment_name_or_id:
                environment = Environment.get_environment(project, from_environment_name_or_id)
            elif environment.is_challenger():
                environment = environment.get_promotes_to_environment()
            component_config = None
            component_config_path = args.get('--component-config')
            if component_config_path is not None:
                if not os.path.isfile(component_config_path):
                    raise KorticalKnownException(f"Unable to find the component config path [{component_config_path}] from the folder [{os.getcwd()}]")
                with open(component_config_path) as f:
                    component_config = f.read()
            challenger_environment = environment.create_challenger(challenger_name, component_config)
            print_success(f"Challenger environment [{challenger_environment.name}] created.")
            challenger_environment.select()
            display_selected_environment(challenger_environment, True)
            display_list_component_instances(project, challenger_environment)

    elif args['kortical-config']:
        _, environment = check_project_and_environment_selected()

        if args['get']:
            display_selected_environment(environment)
            display_kortical_config_list(environment)

        if args['set']:
            kortical_config = {args['<key>']: args['<value>']}
            environment.set_kortical_config(kortical_config)
            display_selected_environment(environment)
            display_kortical_config_list(environment)

        if args['inherit']:
            kortical_config = {args['<key>']: None}
            environment.set_kortical_config(kortical_config)
            display_selected_environment(environment)
            display_kortical_config_list(environment)

    elif args['wait-for-components']:
        timeout = int(args['--timeout']) if args['--timeout'] is not None else None
        project, environment = check_project_and_environment_selected()
        print_title(f'Waiting for components in [{environment.name}] to reach the [RUNNING] state.')
        display_list_component_instances(project, environment)
        environment.wait_for_all_components_ready(timeout_seconds=timeout)
        print_success(f'All components in environment [{environment.name}] running and ready to serve requests.')

    elif args['component-config']:
        _, environment = check_project_and_environment_selected()

        if args['set']:
            component_config_path = args['--component-config']
            if not os.path.isfile(component_config_path):
                raise KorticalKnownException(f"Unable to find the component config path [{component_config_path}] from the folder [{os.getcwd()}]")
            with open(component_config_path) as f:
                component_config = f.read()
            environment.set_component_config(component_config)
            print_success(f"Component config set for project [{project.name}], environment [{environment.name}]")
            display_list_component_instances(project, environment)
