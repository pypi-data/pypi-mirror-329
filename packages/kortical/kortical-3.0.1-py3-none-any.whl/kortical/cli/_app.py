import os
from datetime import datetime

from kortical.api.app import App, get_local_apps
from kortical.api.app_version import AppVersion
from kortical.api.enums import ComponentType
from kortical.api.component_instance import ComponentInstanceState
from kortical.cli._environment import non_challenger_environment_warning
from kortical.cli._component import _user_prompt_component
from kortical.cli._cmd_registry import command
from kortical.cli.helpers.component_helpers import display_list_component_instances_urls
from kortical.helpers import load_from_path, check_project_and_environment_selected
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_info, print_title, print_success, print_warning, display_list, \
    print_error, user_prompt_input, user_prompt_option, user_prompt_yes_no, print_options, display_list


def _user_prompt_local_app(app_directory, app_names):
    local_apps = sorted(list(get_local_apps(app_directory).keys()))

    # Prompt for user input (they can choose to deploy one app or all apps)
    if app_names is None:
        num_local_apps = len(local_apps)
        if num_local_apps > 1:
            local_app_index_map = {f"{k}": v for k, v in enumerate(local_apps, start=1)}
            local_app_index_map[f"{num_local_apps + 1}"] = 'all'
            print_options(f"Apps found in local directory [{app_directory}]:", local_app_index_map)
            app_names = user_prompt_option("Please select an option:", local_app_index_map)
        elif num_local_apps == 1:
            app_names = local_apps[0]

        return [app_names]

    # Validate comma-separated list of app names
    else:
        try:
            app_names = app_names.split(',')
        except:
            raise KorticalKnownException("App names must be passed in as a comma-separated list.")

        for name in app_names:
            if name not in local_apps:
                raise KorticalKnownException(f"App name [{name}] was not found. Valid options are {local_apps}. "
                                             f"To deploy all apps, run [kortical app deploy --all].")
        return app_names


def _user_prompt_template(template_name):
    if template_name is None:
        template_names = App.list_templates()
        template_index_map = {f"{k}": v for k, v in enumerate(template_names, start=1)}
        print_options("Available app templates:", template_index_map)
        template_name = user_prompt_option("Please select an option:", template_index_map)
    return template_name


def _user_prompt_app(app_name_or_id):
    # Prompt user
    if app_name_or_id is None:
        apps = App.list()
        print_title(f"Apps:")
        display_list(apps)

        options = [f"{a.id}" for a in apps] + [f"{a.name}" for a in apps]
        app_name_or_id = user_prompt_option("Please enter an app name or ID:", options)

    # Get app
    app = App.get_app(app_name_or_id)
    if app is None:
        raise KorticalKnownException(f"App [{app_name_or_id}] does not exist. "
                                     f"Run [kortical app list] to see valid names or IDs.")
    return app


def _user_prompt_app_version(app, version_name_or_id):
    # Prompt user
    if version_name_or_id is None:
        versions = app.list_versions(include_created_by=True)
        print_title(f"Versions for app [{app.name}]:")
        display_list(versions)

        version_ids = [f"{v.id}" for v in versions]
        version_names = [f"{v.version}" for v in versions if v.version is not None]
        options = version_ids + version_names

        version_name_or_id = user_prompt_option("Please enter a version name or ID:", options)

    # Get version
    app_version = app.get_version(version_name_or_id)
    if app_version is None:
        raise KorticalKnownException(f"App version [{version_name_or_id}] does not exist. "
                                     f"Run [kortical app version list] to see valid names or IDs.")
    return app_version


@command('app')
def command_app(args):
    """
Controls creation and deployment of apps on the Kortical platform.

Definitions:

App                 A term used to refer to a codebase/application hosted on Kortical. The codebase may be created from
                    one of the templates provided, and the app is added to Kortical for the first time when you deploy
                    to any environment within a project.
App version         A new version of an app, created every time the code is deployed to Kortical. App versions are not
                    assigned a number unless you set one using [kortical app set-default-version].
Component           A deployment of an app or model; components are found within an environment of a Kortical project.
App Config          External settings that may be used to alter the behaviour of an app.
                    App config may be set on a version or component level.

usage:
    kortical app [-h]
    kortical app list-templates
    kortical app list
    kortical app create [-f] <app-base-name> [--template=<template-name>] [--target-dir=<target-dir>]
    kortical app deploy [-f] [--all | <app-names>] [--timeout=<timeout>] [--plain-text]
    kortical app logs <component-name-or-instance-id> [--replica=<replica>]
    kortical app delete [-f] [<app-name-or-id>]
    kortical app restart [<app-name-or-id>] [--timeout=<timeout>]
    kortical app config get [<component-name-or-instance-id>]
    kortical app config set [<component-name-or-instance-id>] --config=<file-path> [--no-restart]
    kortical app set-default-version [<app-name-or-id> <version-name-or-id>]
    kortical app versions list [<app-name-or-id>]
    kortical app versions describe [<app-name-or-id> <version-name-or-id>] [--description=<description>]
    kortical app versions delete [<app-name-or-id> <version-name-or-id>]
    kortical app versions config get [<app-name-or-id> <version-name-or-id>]
    kortical app versions config set [<app-name-or-id> <version-name-or-id>] --config=<file-path>

options:
    -h, --help                          Display help.
    -f, --force                         Execute command without confirmation.
    -j, --json                          Print the output of the command as json.
    <app-base-name>                     Name of your new app folder (i.e codebase which can be set up as a Github repository).
    <template-name>                     Name of the template you want to use for your project; see [kortical app list-templates].
    <target-dir>                        Location where you want to create an app folder.
    <app-names>                         Comma-separated list of apps you want to deploy.
    <app-name-or-id>                    Name or ID used to refer to an app; run [kortical app list] to view this.
    <version-name-or-id>                Name or ID used to refer to a version; run [kortical app version list] to view this.
    <component-name-or-instance-id>     Name of the app or the ID for the specific app instance; run [kortical component list] to view this.
    <replica>                           Executes the command with respect to a specific k8s pod (e.g app-0, app-1, app-2...).


commands:
    list-templates          Returns a list of Kortical templates, each intended as a starting point
                            for developing your own custom apps.
    list                    Returns a full list of apps that are deployed across Kortical.
    create                  Creates a new codebase with the specified app name; defaults to your current working directory.
    deploy                  Deploys your app(s) to the selected project/environment on Kortical (this command also
                            build/push of Docker images). This command should be run at the root of an app folder.
    logs                    Returns logs for a deployed app in the selected project/environment.
    delete                  Deletes an app from Kortical (this includes all app versions and instances found in any projects).
    restart                 Restarts the deployed app. This might be necessary to reload the application configuration in your code.
    config                  Get/set configuration settings on a component level (i.e for a deployed app).
                            Setting will trigger a restart by default, so that the app uses the updated config.
    set-default-version     Assigns an official version number to an app version (refer to definition above).
    version                 List the versions for a given app, and get/set configuration settings on a version level
                            (i.e any time the version is deployed to a environment, it will contain this config)


aliases:
    app                 a apps
    config              cfg
    versions            v vrs version
    """

    app_directory = os.getcwd()
    local_apps = get_local_apps(app_directory)

    if args['list-templates']:
        template_names = App.list_templates()
        print_title("Available app templates:")
        for name in template_names:
            print_info(name)

    elif args['list'] and not args['versions']:
        apps = App.list()
        print_title("Apps deployed to Kortical:")
        display_list(apps)

        if len(local_apps) > 0:
            print_title(f"Apps found in local directory [{app_directory}]:")
            for app in list(local_apps.keys()):
                print_info(app)

    elif args['create']:
        app_name = args['<app-base-name>']
        template_name = _user_prompt_template(args['--template'])

        if not args['--force'] and App.get_app(app_name) is not None:
            print_warning("WARNING: This folder name clashes with an existing app deployed to Kortical.\n"
                          "Deploying from this folder will create new versions of the existing app "
                          "(if this is unintended, use a different name).")
            should_continue = user_prompt_yes_no("Are you sure you want to continue creating this app folder? [y/N]\n")
            if not should_continue:
                raise KorticalKnownException("App create cancelled.")

        App.create_app_folder_from_template(app_name, template_name, args['--target-dir'])

    elif args['deploy']:
        now = datetime.now()
        formatted_time = now.strftime("%I:%M%p on %d of %b %Y").replace('AM', 'am').replace('PM', 'pm')
        print_info(f"Current time [{formatted_time}]")
        project, environment = check_project_and_environment_selected()
        app_directory = os.getcwd()
        app_names = ['all'] if args['--all'] else _user_prompt_local_app(app_directory, args.get('<app-names>'))
        timeout = int(args['--timeout']) if args['--timeout'] is not None else 180

        # Warn if not in challenger
        if not args['--force'] and not environment.is_challenger():
            should_add = non_challenger_environment_warning(environment, "deploy an app to")
            if not should_add:
                print_error("App deploy cancelled.")
                return

        if args['--plain-text']:
            plain_text = True
        else:
            plain_text = False

        # Deploy + wait
        if app_names == ['all']:
            App.deploy_app('all', app_directory, environment, plain_text=plain_text)
            print_info(f"Waiting for environment [{environment.name}] to be ready...")
            environment.wait_for_all_components_ready(timeout_seconds=timeout)
        else:
            for app_name in app_names:
                App.deploy_app(app_name, app_directory, environment, plain_text=plain_text)
            for app_name in app_names:
                app_instance = environment.get_component_instance(app_name, component_type='app')
                app_instance.wait_for_status('Running', timeout_seconds=timeout)

        app_instances = environment.list_component_instances(component_type='app')
        print_success(f"Deployment complete!")
        print_title(f"Apps deployed to environment [{environment.name}]:")
        display_list(app_instances)
        display_list_component_instances_urls(app_instances, project, environment)

    elif args['logs']:
        project, environment = check_project_and_environment_selected()
        app_instance = _user_prompt_component(project, environment, args['<component-name-or-instance-id>'], ComponentType.APP)
        replica = args['--replica'] if args['--replica'] is not None else 0
        logs = app_instance.get_logs(replica)
        print_success(f"Logs for project [{project.name}], environment [{environment.name}], component [{app_instance.name}-{replica}]:")
        print(logs)

    elif args['delete'] and not args['versions']:
        app = _user_prompt_app(args['<app-name-or-id>'])

        if not args['--force']:
            print_warning(f"WARNING: The app [{app.name}] and all of its versions will be deleted from Kortical.")
            should_delete = user_prompt_yes_no(f"Are you sure you want to continue? [y/N]\n")
            if not should_delete:
                print_error("App delete cancelled.")
                return

        app.delete()
        print_success(f"App [{app.name}] deleted successfully.")

    elif args['restart']:
        timeout = int(args['--timeout']) if args['--timeout'] is not None else None
        project, environment = check_project_and_environment_selected()
        app_instance = _user_prompt_component(
            project,
            environment,
            args['<app-name-or-id>'],
            ComponentType.APP
        )
        app_instance.restart()
        print_info(f"Waiting for app [{app_instance.name}] to restart.")
        app_instance.wait_for_status(ComponentInstanceState.PENDING, timeout_seconds=timeout)
        app_instance.wait_for_status(ComponentInstanceState.RUNNING, timeout_seconds=timeout)
        print_success("Restart complete!")

    elif args['config'] and not args['versions']:
        project, environment = check_project_and_environment_selected()
        app_instance = _user_prompt_component(project, environment, args['<component-name-or-instance-id>'], ComponentType.APP)

        if args['get']:
            config = app_instance.get_app_config()
            print_success(f"Config for project [{project.name}], environment [{environment.name}], component [{app_instance.name}]:")
            print_info(str(config))

        if args['set']:
            app_config = load_from_path(args['--config'])
            restart = False if args['--no-restart'] else True
            config = app_instance.set_app_config(app_config, restart)
            print_success(f"Config set for project [{project.name}], environment [{environment.name}], component [{app_instance.name}]:")
            print_info(str(config))
            if restart:
                print_info(f"Waiting for app [{app_instance.name}] to restart.")
                app_instance.wait_for_status(ComponentInstanceState.PENDING)
                app_instance.wait_for_status(ComponentInstanceState.RUNNING)
                print_success("Restart complete!")

    elif args['set-default-version']:
        app = _user_prompt_app(args['<app-name-or-id>'])
        app_version = _user_prompt_app_version(app, args['<version-name-or-id>'])

        # Set version
        app_version = app.set_default_version(app_version)

        print_success(f"Set [{app_version}] as the default version for app [{app.name}]:")
        print_title("App:")
        display_list(app)
        print_title("Version:")
        display_list(app_version)

    elif args['versions']:
        app = _user_prompt_app(args['<app-name-or-id>'])

        if args['list']:
            print_title("App:")
            display_list(app)
            print_title(f"App Versions:")
            display_list(app.list_versions(include_created_by=True))

        elif args['describe']:
            app_version = _user_prompt_app_version(app, args['<version-name-or-id>'])
            description = args['--description'] if args['--description'] is not None else user_prompt_input('Please provide a description:')
            app_version.set_description(description)
            print_success(f"Description updated for app [{app.name}], version [{app_version}]:")
            print_info(description)

        elif args['delete']:
            app_version = _user_prompt_app_version(app, args['<version-name-or-id>'])
            app.delete_version(app_version)
            print_success(f"App version [{app_version}] deleted.")

        elif args['config']:
            app_version = _user_prompt_app_version(app, args['<version-name-or-id>'])

            if args['get']:
                app_config = app_version.get_app_version_config()
                print_success(f"App config for app [{app.name}], version [{app_version}]:")
                print_info(str(app_config))

            elif args['set']:
                old_version_id_list = [v.id for v in AppVersion.list(app)]

                new_app_config = app_version.set_app_version_config(load_from_path(args['--config']))

                # Find new app version if it was created
                new_version_id_list = [v.id for v in AppVersion.list(app)]

                if new_version_id_list != old_version_id_list:
                    new_version_id = list(set(new_version_id_list) - set(old_version_id_list))[0]
                    new_version = AppVersion.get_version(app, new_version_id)
                    print_info(f"New version created, app [{app.name}], version [{new_version}]. App config:")
                else:
                    print_success(f"App config set for app [{app.name}], version [{app_version}]:")
                print_info(str(new_app_config))
