from flask import Response, request
import logging
import pandas as pd


from kortical.app import get_app_config
from kortical.app import requests
from module_placeholder.authentication import safe_api_call

logger = logging.getLogger(__name__)

app_config = get_app_config(format='yaml')
model_name = app_config['model_name']


def register_routes(app):

    @app.route('/health', methods=['get'])
    def health():
        return {"result": "success"}

    @app.route('/predict', methods=['post'])
    @safe_api_call
    def predict():
        input_text = request.json['input_text']
        if not isinstance(input_text, list):
            input_text = [input_text]
        request_data = {
            'Text': input_text
        }
        df = pd.DataFrame(request_data)
        # Do custom pre-processing (data cleaning / feature creation)
        try:
            df = requests.predict(model_name, df)
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                return Response(
                    f"Error model [{model_name}] not found. Has the model been trained and has it had enough time to start?")
            raise
        # Do custom post-processing
        predicted_category = df['predicted_Category']

        if len(predicted_category) == 1:
            predicted_category = predicted_category[0]

        return Response(predicted_category)
