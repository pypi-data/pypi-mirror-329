from kortical.api.worker_group import WorkerGroup
from kortical.cli._cmd_registry import command
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_warning, print_title, print_question, print_success, print_error, display_list, display_string_list, user_prompt_option, user_prompt_yes_no


def _user_prompt_worker_group(worker_group_name_or_id):
    # Prompt user
    if worker_group_name_or_id is None:
        worker_groups = WorkerGroup.list()
        print_title(f"Worker groups:")
        display_list(worker_groups)

        options = [f"{w.id}" for w in worker_groups] + [f"{w.name}" for w in worker_groups]
        worker_group_name_or_id = user_prompt_option("Please enter a worker group name or ID:", options)

    # Get worker group
    worker_group = WorkerGroup.get_worker_group(worker_group_name_or_id)
    if worker_group is None:
        raise KorticalKnownException(f"Worker group [{worker_group_name_or_id}] does not exist."
                                     f"Run [kortical worker list] to see valid names or IDs.")
    return worker_group


def _user_prompt_worker_type():
    worker_types = WorkerGroup.list_worker_types()
    display_string_list('worker_type', worker_types)
    default_worker_type = WorkerGroup.default_worker_type()
    selected_worker_type = user_prompt_option(f"Please enter the exact name of a worker type from the list above, "
                                              f"or leave blank to use the default [{default_worker_type}]:",
                                              worker_types + [''])
    if len(selected_worker_type) == 0:
        selected_worker_type = WorkerGroup.default_worker_type()

    return selected_worker_type


def _user_prompt_size(size=None):
    # Prompt user
    if size is None:
        print_question("How many workers would you like in the worker group?")
        size = input()
        if not size.isdecimal():
            raise KorticalKnownException(f"<size> is expected to be a positive integer value.")
    try:
        size = int(size)
    except:
        raise KorticalKnownException(f"<size> is expected to be a positive integer value.")
    if size < 0:
        raise KorticalKnownException(f"<size> is expected to be a positive integer value.")

    return size


def display_list_worker_groups():
    worker_groups = WorkerGroup.list()
    print_title("Worker Groups:")
    display_list(worker_groups)
    return worker_groups


def display_worker_group(worker_group, is_success=False):
    if is_success:
        print_ = print_success
    else:
        print_ = print_title
    print_(f"Worker Group [{worker_group.name}].")
    display_list(worker_group)


@command('worker')
def command_app(args):
    """
Controls creation and management of worker groups on Kortical.

Definitions:

Worker Group        A set of computers of a given specification (e.g number of cores, RAM, GPU). You can configure various tasks, projects
                    and environments to run on a specific worker group. For example, you might want to dedicate one worker group for
                    training models and another for a Production environment, so performance by one is not affected by the other.


usage:
    kortical worker [-h]
    kortical worker list
    kortical worker resize [<worker-group-name-or-id> <size>]
    kortical worker create <worker-group-name>
    kortical worker delete [-f] [<worker-group-name-or-id>]


options:
    -h, --help              Display help.
    -f, --force             Execute command without confirmation.
    <size>                  Number of computers in worker group (integer).


commands:
    list                Returns a list of worker groups available for use.
    resize              Sets a new desired size for a worker group.
    create              Creates a new worker group.
    delete              Deletes an existing worker group.


aliases:
    worker              w workers
    """

    if args['list']:
        display_list_worker_groups()

    elif args['resize']:
        worker_group = _user_prompt_worker_group(args['<worker-group-name-or-id>'])
        size = _user_prompt_size(args['<size>'])
        worker_group = worker_group.resize(size)
        display_worker_group(worker_group, is_success=True)

    elif args['create']:
        worker_group_name = args.get('<worker-group-name>')
        worker_type = _user_prompt_worker_type()
        worker_size = _user_prompt_size()

        WorkerGroup.create_worker_group(worker_group_name, worker_type, worker_size)
        display_list_worker_groups()
        print_success(f"Worker group [{worker_group_name}] is being created; "
                      f"this may take time to scale up and become fully operational.")

    elif args['delete']:
        worker_group = _user_prompt_worker_group(args['<worker-group-name-or-id>'])

        if not args['--force']:
            display_list_worker_groups()
            print_warning(f"WARNING: The worker group [{worker_group.name}] will be deleted.")
            should_delete = user_prompt_yes_no(f"Are you sure you want to continue? [y/N]\n")
            if not should_delete:
                print_error("Worker group delete cancelled.")
                return

        worker_group.delete()
        print_success(f"Worker group [{worker_group.name}] deleted.")
