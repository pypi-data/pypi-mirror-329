import os
from pathlib import Path
import shutil
import traceback
import uuid

from kortical.cloud_api_app_templates import get_templates_directory
from kortical.docker.docker import get_container_repo
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_info


APP_NAME_PLACEHOLDER = 'app_name_placeholder'                       # Name of the yml file (i.e what the app name will be in Kortical)
MODULE_NAME_PLACEHOLDER = 'module_placeholder'                      # Normal replacement in .py files (needs underscores + lowercase)
K8S_NAME_PLACEHOLDER = 'k8s_name_placeholder'                       # Contents of yml file (needs dashes + lowercase)
CONTAINER_REPO_PLACEHOLDER = 'cloud_container_repo_placeholder'     # Company container registry
FLASK_KEY_PLACEHOLDER = 'flask_key_placeholder'


def _replace_path_name(path, placeholder, target_str):
    new_path = path
    if placeholder in path:
        new_path = path.replace(placeholder, target_str)
        os.replace(path, new_path)
    return new_path


def _replace_chars(text, chars, new_char):
    for char in chars:
        text = text.replace(char, new_char)
    return text.lower()


def _replace_file_contents(original_file_contents, placeholder_str, target_str, container_repo):
    target_str_with_dashes_lowercase = _replace_chars(target_str, ['_', ' '], '-').lower()
    target_str_with_underscores_lowercase = _replace_chars(target_str, ['-', ' '], '_').lower()

    original_file_contents = original_file_contents.replace(placeholder_str, target_str)
    original_file_contents = original_file_contents.replace(APP_NAME_PLACEHOLDER, target_str)
    original_file_contents = original_file_contents.replace(MODULE_NAME_PLACEHOLDER, target_str_with_underscores_lowercase)
    original_file_contents = original_file_contents.replace(K8S_NAME_PLACEHOLDER, target_str_with_dashes_lowercase)
    original_file_contents = original_file_contents.replace(CONTAINER_REPO_PLACEHOLDER, container_repo)
    original_file_contents = original_file_contents.replace(FLASK_KEY_PLACEHOLDER, str(uuid.uuid4()))

    return original_file_contents


def replace_placeholders(base_path, placeholder_str, target_str, container_repo):
    target_str_with_underscores_lowercase = _replace_chars(target_str, ['-', ' '], '_').lower()

    new_path = _replace_path_name(base_path, placeholder_str, target_str)
    new_path = _replace_path_name(new_path, APP_NAME_PLACEHOLDER, target_str)
    new_path = _replace_path_name(new_path, MODULE_NAME_PLACEHOLDER, target_str_with_underscores_lowercase)

    try:
        # Skip files
        if os.path.basename(new_path) in ('.DS_Store') or \
           os.path.splitext(new_path)[1].lower() in ('.xls', '.xlsx', '.csv', '.png', '.svg', '.jpg', '.jpeg', '.ico'):
            # Don't try and read / replace the contents of excel files or images
            return

        # Replace contents of file
        if os.path.isfile(new_path):
            with open(new_path, 'r') as file_in:
                original_contents = file_in.read()
            with open(new_path, 'w') as file_out:
                new_file_content = _replace_file_contents(original_contents, placeholder_str, target_str, container_repo)
                file_out.write(new_file_content)
        else:
            # These folders are generated during the wheel build
            if Path(new_path).name == '__pycache__':
                shutil.rmtree(new_path)
            # Recurse
            else:
                sub_items = os.listdir(new_path)
                for item in sub_items:
                    next_path = os.path.join(new_path, item)
                    replace_placeholders(next_path, placeholder_str, target_str, container_repo)
    except Exception as e:
        raise Exception(f"Error replacing placeholders in file [{new_path}]") from e


def create_app_folder_from_template(template_name, app_name, working_dir=None):
    # Define from/to directories
    template_directory = os.path.join(get_templates_directory(), template_name)
    if not working_dir:
        working_dir = os.getcwd()
    app_directory = os.path.join(working_dir, app_name)

    # Get company container registry
    container_repo = get_container_repo()

    # Check destination path is clear
    if os.path.exists(app_directory):
        raise KorticalKnownException(f'Directory already exists at [{app_directory}]. '
                                     f'Please remove this directory, or use a different app folder name.')

    # Copy over and render app template
    try:
        shutil.copytree(template_directory, app_directory)
        print_info(f'Retrieving template [{template_name}] to current working directory. '
                   f'Path to template project will be [{app_directory}].')
        replace_placeholders(app_directory, template_name, app_name, container_repo)
        return app_directory
    except Exception as e:
        print(traceback.format_exc())
        if os.path.isdir(app_directory):
            shutil.rmtree(app_directory)
        raise
