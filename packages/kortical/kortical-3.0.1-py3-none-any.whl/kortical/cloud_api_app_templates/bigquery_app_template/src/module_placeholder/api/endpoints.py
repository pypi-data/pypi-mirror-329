from flask import Response
import logging

from kortical.app import get_app_config
from kortical.app import requests

from module_placeholder.api.http_status_codes import HTTP_OKAY
from module_placeholder.authentication import safe_api_call
from module_placeholder.bigquery.bigquery import create_dataframe_from_bigquery, insert_dataframe_into_bigquery

logger = logging.getLogger(__name__)

app_config = get_app_config(format='yaml')
model_name = app_config['model_name']


def register_routes(app):

    @app.route('/health', methods=['get'])
    def health():
        return {"result": "success"}

    @app.route('/update_bigquery', methods=['get'])
    @safe_api_call
    def update_bigquery():
        df = create_dataframe_from_bigquery()
        df = requests.predict(model_name, df)
        insert_dataframe_into_bigquery(df)
        return Response("Success!")
