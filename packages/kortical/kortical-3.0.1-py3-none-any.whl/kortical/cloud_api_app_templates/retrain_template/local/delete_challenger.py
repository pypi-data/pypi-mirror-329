from google.cloud import bigquery
import sys

from kortical.app import get_app_config
from kortical.api.environment import Environment

from module_placeholder.bigquery.bigquery import client, credentials
from module_placeholder.constants import SELECTED_PROJECT, SELECTED_ENVIRONMENT

app_config = get_app_config(format='yaml')


gcp_project_id = credentials.project_id


def delete_challenger_database_and_environment(challenger_environment):

    challenger_dataset_name = f"{app_config['bigquery']['dataset_name']}_{challenger_environment.name.lower()}"

    # Delete challenger database if exists
    challenger_dataset_ref = bigquery.DatasetReference(gcp_project_id, challenger_dataset_name)
    client.delete_dataset(challenger_dataset_ref, delete_contents=True, not_found_ok=True)

    # Delete challenger environment
    challenger_environment.delete()


if __name__ == '__main__':

    # Check if arguments are provided, else use default values
    environment = Environment.get_environment(SELECTED_PROJECT, sys.argv[1]) if len(sys.argv) > 1 else SELECTED_ENVIRONMENT

    if not environment.is_challenger():
        raise Exception("You must have a challenger environment selected.")

    delete_challenger_database_and_environment(environment)
