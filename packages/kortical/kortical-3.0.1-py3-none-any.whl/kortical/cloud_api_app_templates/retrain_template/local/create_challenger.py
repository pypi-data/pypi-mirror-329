import os
from google.cloud import bigquery
import sys

from kortical.app import get_app_config
from kortical.api.environment import Environment

from kortical.helpers.print_helpers import print_info, print_success
from module_placeholder.bigquery.bigquery import client, credentials
from module_placeholder.constants import SELECTED_PROJECT, SELECTED_ENVIRONMENT
from module_placeholder.helpers.root_dir import from_root_dir

app_config = get_app_config(format='yaml')


gcp_project_id = credentials.project_id


def create_challenger_database_and_environment(challenger_name, source_environment, component_config):

    source_dataset_name = f"{app_config['bigquery']['dataset_name']}_{source_environment.name.lower()}"
    challenger_dataset_name = f"{app_config['bigquery']['dataset_name']}_{challenger_name}"

    # Delete challenger database if exists and recreate it blank.
    challenger_dataset_ref = bigquery.DatasetReference(gcp_project_id, challenger_dataset_name)
    client.delete_dataset(challenger_dataset_ref, delete_contents=True, not_found_ok=True)
    challenger_dataset = bigquery.Dataset(challenger_dataset_ref)
    challenger_dataset.location = "europe-west2"
    client.create_dataset(challenger_dataset, exists_ok=True)

    print_info(f"Creating challenger database [{challenger_dataset_name}], cloned from [{source_dataset_name}]:")

    schema_dir_path = from_root_dir('src/module_placeholder/bigquery/schemas')
    tables_to_copy = [file.split('.')[0] for file in os.listdir(schema_dir_path)]

    for table_name in tables_to_copy:

        print_info(f"\tCopying table [{table_name}]...")

        source_table = client.dataset(source_dataset_name).table(table_name)
        destination_table = client.dataset(challenger_dataset_name).table(table_name)

        copy_job = client.copy_table(source_table, destination_table)
        copy_job.result()

    print_success("Database ready.")

    # Create challenger environment with modified environment config
    print_info(f"Creating challenger environment [{challenger_name}], cloned from [{source_environment.name}]...")
    challenger_environment = source_environment.create_challenger(challenger_name=challenger_name,
                                                                  component_config=component_config)
    challenger_environment.wait_for_all_components_ready()
    print_success("Environment ready.")


if __name__ == '__main__':
    default_challenger_name = 'owen'

    # Check if arguments are provided, else use default values
    challenger_name = sys.argv[1] if len(sys.argv) > 1 else default_challenger_name
    from_environment = Environment.get_environment(SELECTED_PROJECT, sys.argv[2]) if len(sys.argv) > 2 else SELECTED_ENVIRONMENT
    component_config_path = sys.argv[3] if len(sys.argv) > 3 else None
    if component_config_path is not None:
        with open(component_config_path) as f:
            component_config = f.read()
    else:
        component_config = None

    if from_environment.is_challenger():
        raise Exception("You must have one of the main environments selected.")

    create_challenger_database_and_environment(challenger_name, from_environment, component_config)
