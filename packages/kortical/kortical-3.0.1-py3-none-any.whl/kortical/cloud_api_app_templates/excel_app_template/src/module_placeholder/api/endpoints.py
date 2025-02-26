from flask import Response
import logging
from tempfile import NamedTemporaryFile
from kortical.app import get_app_config
from kortical.app import requests

from module_placeholder.api.http_status_codes import HTTP_OKAY
from module_placeholder.authentication import safe_api_call
from module_placeholder.bigquery.bigquery import create_dataframe_from_bigquery
from module_placeholder.excel import create_workbook_from_template

logger = logging.getLogger(__name__)

app_config = get_app_config(format='yaml')
model_name = app_config['model_name']


def register_routes(app):

    @app.route('/health', methods=['get'])
    def health():
        return {"result": "success"}

    @app.route('/latest_churn.xlsx', methods=['get'])
    @safe_api_call
    def get_churn_spreadsheet():
        logger.info('Creating churn spreadsheet.')
        df = create_dataframe_from_bigquery()
        df = requests.predict(model_name, df)
        logger.info("Writing to excel spreadsheet")
        with NamedTemporaryFile() as tempfile:
            create_workbook_from_template(tempfile, "churn_template.xlsx", df)
            logger.debug('Returning excel spreadsheet')
            return Response(tempfile.read(), mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    @app.route('/health')
    def get_health_check():
        return Response('{"result": "success"}', status=HTTP_OKAY, mimetype="application/json")
