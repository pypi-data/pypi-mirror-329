from kortical.api.cronjob import Cronjob
from kortical.cli._cmd_registry import command
from kortical.helpers import check_project_and_environment_selected, load_from_path, format_config
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_success, print_title, print_info, print_error, print_warning, display_list, user_prompt_option, user_prompt_yes_no, user_prompt_input


def _user_prompt_cronjob(project, environment, cronjob_name_or_id):
    # Prompt user
    if cronjob_name_or_id is None:
        cronjobs = Cronjob.list(project, environment)
        print_title(f"Cronjobs:")
        display_list(cronjobs)

        options = [f"{c.id}" for c in cronjobs] + [f"{c.name}" for c in cronjobs]
        cronjob_name_or_id = user_prompt_option("Please enter a cronjob name or ID:", options)

    # Get model
    cronjob = Cronjob.get_cronjob(project, environment, cronjob_name_or_id)
    if cronjob is None:
        raise KorticalKnownException(f"Cronjob [{cronjob_name_or_id}] does not exist. "
                                     f"Run [kortical cronjob list] to see valid names or IDs.")
    return cronjob


@command('cronjob')
def command_app(args):
    """
Controls management of cronjobs on the Kortical Cloud.

Definitions:

Cronjob             An automated task that occurs on a regular schedule.

usage:
    kortical cronjob [-h]
    kortical cronjob list
    kortical cronjob create <cronjob-name> --config=<file-path>
    kortical cronjob update <cronjob-name-or-id> --config=<file-path>
    kortical cronjob delete [-f] [<cronjob-name-or-id>]


options:
    -h, --help              Display help.
    -f, --force             Execute command without confirmation.
    <cronjob-name-or-id>    Name or ID used to refer to a cronjob; run [kortical cronjob list] to view this.
    <file-path>             Path to a config file that specifies how the cronjob runs (i.e what URL it calls + how often);
                            refer to documentation in the platform for an example config file.

commands:
    list                    Returns a list of cronjobs currently running.
    create                  Creates a new cronjob.
    delete                  Deletes a cronjob.


aliases:
    cronjob             cron
    """

    project, environment = check_project_and_environment_selected()

    if args['list']:
        cronjobs = Cronjob.list(project, environment)
        print_title("Cronjobs:")
        display_list(cronjobs)

    elif args['create']:
        cronjob_name = args['<cronjob-name>']
        cronjob_config = format_config(load_from_path(args['--config']), 'yaml')
        time_parameters = cronjob_config['time_parameters']
        url = cronjob_config['url']
        url_headers = cronjob_config.get('url_headers', {})

        cronjob = Cronjob.create_cronjob(project, environment, cronjob_name, time_parameters, url, url_headers)
        print_success(f"Cronjob [{cronjob.name}] created successfully.")
        display_list(cronjob)

    elif args['update']:
        cronjob_config = format_config(load_from_path(args['--config']), 'yaml')
        time_parameters = cronjob_config['time_parameters']
        url = cronjob_config['url']
        url_headers = cronjob_config.get('url_headers', {})

        cronjob = _user_prompt_cronjob(project, environment, args['<cronjob-name-or-id>'])
        cronjob = cronjob.update(time_parameters=time_parameters, url=url, url_headers=url_headers)
        print_success("Cronjob updated:")
        display_list(cronjob)
        
    elif args['delete']:
        cronjob = _user_prompt_cronjob(project, environment, args['<cronjob-name-or-id>'])

        if not args['--force']:
            print_warning(f"WARNING: The cronjob [{cronjob.name}] will be deleted from Kortical.")
            should_delete = user_prompt_yes_no(f"Are you sure you want to continue? [y/N]\n")
            if not should_delete:
                print_error("Cronjob delete cancelled.")
                return

        cronjob.delete()
        print_success(f"Cronjob [{cronjob.name}] deleted successfully.")
