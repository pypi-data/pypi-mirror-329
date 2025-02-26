from datetime import datetime
import git
import os
from pathlib import Path
import re

from kortical.api import advanced
from kortical.api.app_version import AppVersion
from kortical.app import template_helpers
from kortical.docker import docker, image_helpers
from kortical.helpers import check_project_and_environment_selected, load_from_path, KorticalKnownException
from kortical.helpers.print_helpers import print_success, print_info, print_warning


# Most importantly needs to start with a letter so Python module imports work,
# other restrictions (e.g dashes in k8s .yml, lowercase for Docker image name) are satisfied when
# replacing the placeholders in the template.
APP_FOLDER_NAME_REGEX = re.compile(r'^[A-Za-z]([A-Za-z0-9 _-]*[A-Za-z0-9])?$')

APP_TEMPLATES = ["web_app_template",
                 "openai_llm_template",
                 "retrain_template",
                 "bigquery_app_template",
                 "excel_app_template"]


string_patterns = [r"config[/\\]component_config\.yml", r"k8s[/\\].*\.(yml|yaml)"]
patterns = [re.compile(s) for s in string_patterns]


def _validate_app_folder_name(name):

    # Check for template names
    template_names = App.list_templates()
    if name in template_names:
        raise KorticalKnownException(f'App name [{name}] cannot match one of the following template names:\n'
                                     f'{template_names}')

    # The app folder name will also be used for module names, so can't start with a number
    if APP_FOLDER_NAME_REGEX.match(name) is None:
        raise KorticalKnownException(f'App folder name [{name}] must start with an alpha character and can be '
                                     f'separated by dashes, underscores or spaces (e.g. app-123, app_1, AI app).')


def _validate_template_name(template_name):
    template_names = App.list_templates()
    if template_name not in template_names:
        raise KorticalKnownException(f"Invalid template name. Please select from {template_names}.")


def get_local_apps(app_directory=None):
    if app_directory is None:
        app_directory = os.getcwd()

    apps = {}
    k8s_directory = os.path.join(app_directory, 'k8s')
    if os.path.exists(k8s_directory):
        files = os.listdir(k8s_directory)
        apps = {f"{Path(f).stem}": os.path.join(k8s_directory, f) for f in files if f.endswith('.yml') or f.endswith('.yaml')}
    return apps


def assemble_app_description_from_git_commit(app_directory):

    def _is_repo_dirty(repo):
        changed_files = repo.git.status(porcelain=True).split('\n')
        for file_status in changed_files:
            file_path = file_status[3:].strip()
            if not any(bool(pattern.search(file_path)) for pattern in patterns):
                return True
        return False

    try:
        repo = git.Repo(app_directory)
        latest_commit = repo.head.commit
        hash = latest_commit.hexsha[:5]

        # Check if the repo is dirty, ignore component_config + k8s files
        if _is_repo_dirty(repo):
            hash += "+dev"

        description = f"{hash} - {latest_commit.message.strip()}"
    except git.InvalidGitRepositoryError:
        description = None

    return description


class App:

    @classmethod
    def _create_from_json(cls, app_json):
        created = datetime.strptime(app_json['created']['__value__'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        return cls(
            id_=app_json['id'],
            name=app_json['name'],
            created=created,
            created_by=app_json.get('created_by'),
            default_component_version_id=app_json['default_component_version_id']
        ) if app_json else None

    @staticmethod
    def list_templates():
        return APP_TEMPLATES

    @classmethod
    def create_app(cls, app_name):
        app_json = advanced.app.create_app(app_name)
        app = cls._create_from_json(app_json) if app_json else None
        return app

    @classmethod
    def list(cls):
        return [cls._create_from_json(x) for x in advanced.app.list_apps()]

    @classmethod
    def get_app(cls, app_name_or_id):
        app_json = advanced.app.get_app(app_name_or_id)
        app = cls._create_from_json(app_json) if app_json else None
        return app

    @staticmethod
    def create_app_folder_from_template(app_name, template_name, target_directory=None):
        _validate_app_folder_name(app_name)
        _validate_template_name(template_name)

        root_path = template_helpers.create_app_folder_from_template(template_name, app_name, target_directory)
        print_success(f'Created [{template_name}] template for [{app_name}] at [{root_path}].')

    @staticmethod
    def deploy_app(app_name, app_directory=None, environment=None, plain_text=False):
        if app_directory is None:
            app_directory = os.getcwd()
        if environment is None:
            _, environment = check_project_and_environment_selected()

        app_version_description = assemble_app_description_from_git_commit(app_directory)

        # Get local k8s/docker files
        local_apps = get_local_apps(app_directory)
        local_images = docker.get_local_images(app_directory)

        # Validation
        if len(local_apps) == 0:
            raise KorticalKnownException(f"No apps found, are you sure you're in the app directory? "
                                         f"App directory specified: {app_directory}")
        if app_name != 'all' and app_name not in list(local_apps.keys()):
            raise KorticalKnownException(f"App name [{app_name}] was not found. Valid options are {local_apps}")

        # STEP 1: build + push images
        if app_name == 'all':
            # Build + push all images
            docker.build_push(local_images, app_directory, plain_text=plain_text)
            apps_to_deploy = local_apps
        else:
            # Only build + push images relevant to the specified app
            k8s_config_path = local_apps.get(app_name)
            images = [x for x in image_helpers.get_image_names_from_k8(k8s_config_path) if x in local_images]
            docker.build_push(images, app_directory, plain_text=plain_text)
            apps_to_deploy = {f"{app_name}": local_apps.get(app_name)}

        # STEP 2: deploy k8s files (+ app config)
        for name in apps_to_deploy.keys():

            # Read k8s_config and app_config for creating a new version
            k8s_config = load_from_path(os.path.join(app_directory, "k8s", f"{name}.yml"))
            try:
                app_config_dir = os.path.join(app_directory, "config")
                app_config_path = next(os.path.join(app_config_dir, f) for f in os.listdir(app_config_dir)
                                       if
                                       os.path.isfile(os.path.join(app_config_dir, f)) and Path(f).stem == 'app_config')
                app_config = load_from_path(app_config_path)
            except:
                print_warning(f"App config path [{app_directory}/config/app_config.*] was not found. Skipping...")
                app_config = None

            # Create app/app_version/app_instance
            print_info(f'Deploying app [{name}] to environment [{environment}]...')
            app = App.get_app(name)
            if app is None:
                app = App.create_app(name)
            app_version = app.create_version(k8s_config, app_config)
            app_version.set_description(description=app_version_description)
            print_success(f"Created new version [{app_version}].")
            component_instance = environment.create_component_instance(app_version.id)
            print_success(f"Created new component instance [id [{component_instance.id}]].")

    def __init__(self, id_, name, created, default_component_version_id, created_by=None):
        self.id = id_
        self.name = name
        self.default_version = AppVersion.get_version(self, default_component_version_id)
        if created_by:
            self.created_by = created_by
        self.created = created

    def __repr__(self):
        return f"id [{self.id}], name [{self.name}]"

    def create_version(self, k8s_config, app_config=None):
        app_version = AppVersion.create_version(self, k8s_config, app_config)
        return app_version

    def list_versions(self, include_created_by=False):
        app_versions = AppVersion.list(self, include_created_by)
        return app_versions

    def get_version(self, version_name_or_id):
        app_version = AppVersion.get_version(self, version_name_or_id)
        return app_version

    def set_default_version(self, app_version):
        app_version = AppVersion._create_from_json(advanced.app.set_default_app_version(self.id, app_version.id))
        self.default_version = app_version
        return app_version

    def delete_version(self, app_version):
        return advanced.app.delete_app_version(self.id, app_version.id)

    def to_json(self):
        return vars(self)

    def delete(self):
        return advanced.app.delete_app(self.id)
