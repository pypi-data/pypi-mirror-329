from kortical.api.component_instance import ComponentInstance
from kortical.api.enums import ComponentInstanceState, ComponentType
from kortical.cli._cmd_registry import command
from kortical.cli._project import display_selected_project
from kortical.cli._environment import display_selected_environment, non_challenger_environment_warning
from kortical.cli.helpers.component_helpers import display_list_component_instances, display_list_component_instances_urls
from kortical.cli.helpers.kortical_config_helpers import display_kortical_config_list

from kortical.helpers import check_project_and_environment_selected, KorticalKnownException, load_from_path
from kortical.helpers.print_helpers import print_success, display_list, print_warning, print_title, print_error, user_prompt_yes_no, user_prompt_option


def _user_prompt_component(project, environment, component_name_or_instance_id, component_type=None):
    # Prompt user
    if component_name_or_instance_id is None:
        components = ComponentInstance.list(project, environment, component_type, include_created_by=True)
        print_title(f"Components in project [{project.name}], environment [{environment.name}]:")
        display_list(components)

        options = [f"{c.id}" for c in components] + [f"{c.name}" for c in components]
        component_name_or_instance_id = user_prompt_option("Please enter a component instance name or ID:", options)

    # Get component
    component_instance = ComponentInstance.get_component_instance(project, environment, component_name_or_instance_id)
    if component_instance is None:
        raise KorticalKnownException(f"Component [{component_name_or_instance_id}] does not exist. "
                                     f"Run [kortical component list] to see valid names or IDs.")
    return component_instance


@command('component')
def command_app(args):
    """
Controls creation and management of components within a selected project and environment on the Kortical Cloud.

Definitions:

Component          A deployment of an app or model; components are found within an environment of a Kortical project.
                   run [kortical component list] to view everything deployed to the selected environment.
Kortical Config    This allows you to configure settings (i.e worker group, replicas) at
                   the project/environment/component level.

usage:
    kortical component [-h]
    kortical component list [--include-deleted]
    kortical component add [-f] <component-name-or-version-id> [--version=<version_number>]
    kortical component remove [-f] <component-name-or-instance-id> [--timeout=<seconds>]
    kortical component logs <component-name-or-instance-id> [--replica=<replica>]
    kortical component from-config [-f] <file-path>
    kortical component save-config <file-path>
    kortical component get-version-id <component-name-or-instance-id> [--app | --model]
    kortical component kortical-config get [<component-name-or-instance-id>]
    kortical component kortical-config set <key> <value> [<component-name-or-instance-id>]
    kortical component kortical-config inherit <key> [<component-name-or-instance-id>]


options:
    -h, --help                          Display help.
    -f, --force                         Execute command without confirmation.
    <component-name-or-version-id>      Name of the component or ID for the specific component version;
                                        run [kortical model version list] or [kortical app version list] to view this.
                                        If you just give a name it will use the default version.
    <component-name-or-instance-id>     Name of the component or ID for the specific component instance;
                                        run [kortical component list] to view this.


commands:
    list                Returns a list of components within the selected project/environment.
    add                 Adds a component to the environment.
    remove              Removes a component from the environment. This does not affect other environments
                        with deployments of the same app/model.
    logs                Returns logs for the component; currently only supported for apps.
    from-config         Configures the components for the selected environment from a component config file.
                        (NB: this will remove all current components not in the new config.)
    save-config         Saves the component configuration for the selected environment.
    get-version-id      Returns the component version ID for the specified component.
    kortical-config     Adjust Kortical config at the component level.


aliases:
    component           c cpt components
    """

    project, environment = check_project_and_environment_selected()

    if args['list']:
        include_deleted = True if args['--include-deleted'] else False
        display_selected_project(project)
        display_selected_environment(environment)
        component_instances = display_list_component_instances(project, environment, include_deleted=include_deleted)
        display_list_component_instances_urls(component_instances, project, environment)

    elif args['add']:
        component_name_or_version_id = args['<component-name-or-version-id>']
        display_selected_project(project)
        display_selected_environment(environment)

        if not args['--force'] and not environment.is_challenger():
            should_add = non_challenger_environment_warning(environment, "add a component to")
            if not should_add:
                print_error("Component add cancelled.")
                return

        component_instance = ComponentInstance.create_component_instance(project, environment, component_name_or_version_id)
        print_success("Component:")
        display_list(component_instance)

    elif args['remove']:
        timeout_seconds = int(args['--timeout']) if args['--timeout'] is not None else 60
        component_instance = _user_prompt_component(project, environment, args['<component-name-or-instance-id>'])

        if not args['--force'] and not environment.is_challenger():
            should_remove = non_challenger_environment_warning(environment, "remove a component from")
            if not should_remove:
                print_error("Component remove cancelled.")
                return

        print_warning(f"Removing component [{component_instance.name}] from environment [{environment.name}]...")
        component_instance.delete()
        component_instance.wait_for_status(ComponentInstanceState.TERMINATED, timeout_seconds)
        print_success("Component removed.")
        component_instances = ComponentInstance.list(project, environment)
        print_title(f"Components for environment [{environment.name}] in project [{project.name}]:")
        display_list(component_instances)

    elif args['logs']:
        replica = args['--replica'] if args['--replica'] is not None else 0
        app_instance = _user_prompt_component(project, environment, args['<component-name-or-instance-id>'])
        logs = app_instance.get_logs(replica)
        print_success(f"Logs for project [{project.name}], environment [{environment.name}], component [{app_instance.name}-{replica}]:")
        print(logs)

    elif args['from-config']:
        # Ask for confirmation
        if not args['--force']:
            display_selected_environment(environment)
            display_list_component_instances(project, environment)
            print_warning(f"Completing this action will potentially overwrite all of the components and versions for environment [{environment}].")
            should_continue = user_prompt_yes_no(f"Are you sure you want to continue? [y/N]\n")
            if not should_continue:
                print_error("Action cancelled.")
                return

        component_config = load_from_path(args['<file-path>'])
        environment.set_component_config(component_config)
        print_success("Component config set successfully.")

    elif args['save-config']:
        config_file_path = args['<file-path>']
        component_config = environment.get_component_config()
        with open(config_file_path, 'w') as f:
            f.write(component_config)
        print_success("Component config fetched successfully.")

    elif args['get-version-id']:
        component_name_or_instance_id = args['<component-name-or-instance-id>']
        is_app = args.get('--app')
        is_model = args.get('--model')
        component_type = None

        if is_app:
            component_type = ComponentType.APP
        elif is_model:
            component_type = ComponentType.MODEL

        component_instance = ComponentInstance.get_component_instance(project, environment,
                                                                      component_name_or_instance_id,
                                                                      component_type=component_type)
        if component_instance is None:
            raise KorticalKnownException(f"Component instance [{component_name_or_instance_id}] was not found. "
                                         f"To list instances for this environment, run [kortical component list] "
                                         f"and use the ID column from the components table.")
        print(component_instance.version.id)

    if args['kortical-config']:
        component = _user_prompt_component(project, environment, args['<component-name-or-instance-id>'])

        if args['get']:
            display_list(component)
            display_kortical_config_list(component)

        if args['set']:
            kortical_config = {args['<key>']: args['<value>']}
            component.set_kortical_config(kortical_config)
            display_list(component)
            display_kortical_config_list(component)

        if args['inherit']:
            kortical_config = {args['<key>']: None}
            component.set_kortical_config(kortical_config)
            display_list(component)
            display_kortical_config_list(component)
