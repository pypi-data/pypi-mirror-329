import logging

from kortical.app import get_app_config
from kortical.api.project import Project
from kortical.api.environment import Environment

logger = logging.getLogger(__name__)

app_config = get_app_config(format='yaml')

SELECTED_PROJECT = Project.get_selected_project()
SELECTED_ENVIRONMENT = Environment.get_selected_environment(SELECTED_PROJECT)

MODEL_NAME = app_config['model_name']

BIGQUERY_DATASET_NAME = f"{app_config['bigquery']['dataset_name']}_{SELECTED_ENVIRONMENT.name.lower()}"
BIGQUERY_TABLE_NAME = app_config['bigquery']['table_name']
