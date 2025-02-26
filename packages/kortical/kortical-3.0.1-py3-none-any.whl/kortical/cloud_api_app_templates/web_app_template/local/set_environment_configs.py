import os
from kortical.api.project import Project
from module_placeholder.helpers.root_dir import from_root_dir
from kortical.helpers.print_helpers import print_success, print_error

if __name__ == '__main__':
    project = Project.get_selected_project()
    environments = project.list_environments()

    for environment in environments:
        config_path = os.path.join(from_root_dir(os.path.join('config', f"environment_{environment.name.lower()}.yml")))
        if not os.path.isfile(config_path):
            print_error(f"Environment config file [{config_path}] not found for environment [{environment.name}]. Did you perhaps create some custom environments and now need to update the environment config files to match?")
            continue
        with open(config_path, 'r') as f:
            environment_config = f.read()
        environment.set_environment_config(environment_config)
        print_success(f"Environment config set for environment [{environment.name}]")

