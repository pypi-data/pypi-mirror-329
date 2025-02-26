from kortical.api.model import Model
from kortical.cli._cmd_registry import command
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_success, print_title, print_info, print_error, print_warning, display_list, user_prompt_option, user_prompt_yes_no, user_prompt_input


def _user_prompt_model(model_name_or_id):
    # Prompt user
    if model_name_or_id is None:
        models = Model.list()
        print_title(f"Models:")
        display_list(models)

        options = [f"{m.id}" for m in models] + [f"{m.name}" for m in models]
        model_name_or_id = user_prompt_option("Please enter a model name or ID:", options)

    # Get model
    model = Model.get_model(model_name_or_id)
    if model is None:
        raise KorticalKnownException(f"Model [{model_name_or_id}] does not exist. "
                                     f"Run [kortical model list] to see valid names or IDs.")
    return model


def _user_prompt_model_version(model, version_name_or_id):
    # Prompt user
    if version_name_or_id is None:
        versions = model.list_versions()
        print_title(f"Versions for model [{model.name}]:")
        display_list(versions)

        version_ids = [f"{v.id}" for v in versions]
        version_names = [f"{v.version}" for v in versions if v.version is not None]
        options = version_ids + version_names

        version_name_or_id = user_prompt_option("Please enter a version name or ID:", options)

    # Get version
    model_version = model.get_version(version_name_or_id)
    if model_version is None:
        raise KorticalKnownException(f"Model version [{version_name_or_id}] does not exist. "
                                     f"Run [kortical model version list] to see valid names or IDs.")
    return model_version


@command('model')
def command_app(args):
    """
Controls management of models on the Kortical Cloud.

Definitions:

Model               An algorithm that has been trained on a dataset to predict one or more target columns. In Kortical,
                    this term also refers to a workspace in which a collection of candidate models are trained, of which
                    the best one will be deployed to a project + environment.
Model version       These are created during a training run, which can be viewed on the Lab/Leaderboard page in Kortical.
                    Model versions are not assigned a number until they are published.

usage:
    kortical model [-h]
    kortical model list
    kortical model activate [<model-name-or-id>]
    kortical model deactivate [<model-name-or-id>]
    kortical model delete [-f] [<model-name-or-id>]
    kortical model set-default-version [<model-name-or-id> <version-name-or-id>]
    kortical model versions list [<model-name-or-id>]
    kortical model versions describe [<model-name-or-id> <version-name-or-id>] [--description=<description>]
    kortical model versions delete [<model-name-or-id> <version-name-or-id>]
    kortical model versions delete-unpublished [<model-name-or-id>]


options:
    -h, --help              Display help.
    -f, --force             Execute command without confirmation.
    <model-name-or-id>      Name or ID used to refer to a model; run [kortical model list] to view this.
    <version-name-or-id>    Name or ID used to refer to a version; run [kortical model version list] to view this.

commands:
    list                    Returns a list of models available to the user.
    activate                Activate a dormant model.
    deactivate              Deactivate a model; this does not affect any model instances found in Kortical projects/environments.
    delete                  Deletes a model from Kortical (this includes all model versions and instances found in any projects).
    set-default-version     Assigns an official version number to a model version (refer to definition above).
    version                 List/delete versions for a model. Unpublished model versions do not have a version number (e.g v1, v2).


aliases:
    model               m mdl models
    versions            v vrs version
    """

    if args['list'] and not args['versions']:
        models = Model.list(include_created_by=True)
        print_title("Models:")
        display_list(models)

    elif args['activate']:
        model = _user_prompt_model(args['<model-name-or-id>'])
        model.activate()
        print_success(f"Model [{model.name}] activated.")

    elif args['deactivate']:
        model = _user_prompt_model(args['<model-name-or-id>'])
        model.deactivate()
        print_success(f"Model [{model.name}] deactivated.")
        
    elif args['delete'] and not args['versions']:
        model = _user_prompt_model(args['<model-name-or-id>'])

        if not args['--force']:
            print_warning(f"WARNING: The model [{model.name}] and all of its versions will be deleted from Kortical.")
            should_delete = user_prompt_yes_no(f"Are you sure you want to continue? [y/N]\n")
            if not should_delete:
                print_error("Model delete cancelled.")
                return

        model.delete()
        print_success(f"Model [{model.name}] deleted successfully.")
        
    elif args['set-default-version']:
        model = _user_prompt_model(args['<model-name-or-id>'])
        model_version = _user_prompt_model_version(model, args['<version-name-or-id>'])

        # Set version
        model_version = model.set_default_version(model_version, wait_for_ready=False)

        print_success(f"Set [{model_version}] as the default version for model [{model.name}]:")
        print_title("Model:")
        display_list(model)
        print_title("Version:")
        display_list(model_version)

    elif args['versions']:
        # Prompt user for model if undefined
        model = _user_prompt_model(args['<model-name-or-id>'])

        if args['list']:
            print_title("Model:")
            display_list(model)
            print_title(f"Model Versions:")
            display_list(model.list_versions(include_created_by=True))

        elif args['describe']:
            model_version = _user_prompt_model_version(model, args['<version-name-or-id>'])
            description = args['--description'] if args['--description'] is not None else user_prompt_input('Please provide a description:')
            model_version.set_description(description)
            print_success(f"Description updated for model [{model.name}], version [{model_version}]:")
            print_info(description)

        elif args['delete']:
            model_version = _user_prompt_model_version(model, args['<version-name-or-id>'])
            model.delete_version(model_version)
            print_success(f"Model version [{model_version}] deleted.")

        elif args['delete-unpublished']:
            model.delete_unpublished_versions()
            print_success(f"Unpublished versions deleted.")
