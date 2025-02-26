from google.oauth2 import service_account
from google.cloud import bigquery
import json
import logging
import os
import pandas_gbq
import yaml

from kortical.secret import secret

from module_placeholder.constants import BIGQUERY_DATASET_NAME, BIGQUERY_TABLE_NAME
from module_placeholder.helpers.root_dir import from_root_dir

logger = logging.getLogger(__name__)


# Load credentials + client
try:
    service_account_key = json.loads(secret.get("bigquery_service_account_key"))
    credentials = service_account.Credentials.from_service_account_info(
        info=service_account_key, scopes=["https://www.googleapis.com/auth/cloud-platform"],
    )
except:
    raise Exception("Failed to load credentials for Bigquery; "
                    "check that the secret 'bigquery_service_account_key' has been set in Kortical.")

client = bigquery.Client(credentials=credentials, project=credentials.project_id)


GCP_PROJECT_ID = credentials.project_id
dataset_id = f'{GCP_PROJECT_ID}.{BIGQUERY_DATASET_NAME}'
table_id = f'{dataset_id}.{BIGQUERY_TABLE_NAME}'


def create_dataset():

    dataset = bigquery.Dataset(dataset_id)
    dataset.location = 'europe-west2'
    dataset = client.create_dataset(dataset)
    logging.info(f'Created dataset [{dataset_id}]')
    return dataset


def _process_raw_schema(raw_schema):
    schema = []
    raw_d_type_to_bq_dtype = {
        'string': 'STRING',
        'boolean': 'BOOLEAN',
        'timestamp': 'TIMESTAMP',
        'date': 'DATE',
        'integer': 'INTEGER',
        'float': 'FLOAT'
    }
    raw_mode_to_mode = {
        'required': 'REQUIRED',
        'optional': 'NULLABLE'}
    for field in raw_schema:
        schema.append(
            bigquery.SchemaField(field['field'],
                                 raw_d_type_to_bq_dtype[field['d_type']],
                                 raw_mode_to_mode[field['mode']])
        )
    return schema


def create_tables():
    schema_dir_path = from_root_dir('src/module_placeholder/bigquery/schemas')
    filenames = os.listdir(schema_dir_path)

    for filename in filenames:
        table_name = filename.split('.')[0]
        schema_path = os.path.join(schema_dir_path, filename)
        with open(schema_path, 'r') as f:
            raw_schema = yaml.safe_load(f)
        schema = _process_raw_schema(raw_schema)

        table_id = f'{dataset_id}.{table_name}'
        table = bigquery.Table(table_id, schema=schema)
        table = client.create_table(table)
        logging.info(f'Created table {GCP_PROJECT_ID}.{table.dataset_id}.{table.table_id}')



### HELPERS


def get_dataframe_from_bigquery():
    selected_rows_query = f"""SELECT * FROM `{table_id}`"""
    selected_rows = client.query(selected_rows_query).to_dataframe()
    return selected_rows


def append_dataframe_to_bigquery(df):
    pandas_gbq.to_gbq(
        df,
        table_id,
        if_exists='append',
        credentials=credentials
    )
