from flask import Response

from kortical.api import superhuman_calibration
from kortical.app import get_app_config
from kortical.app import requests

from module_placeholder.workflows import common

app_config = get_app_config(format='yaml')
target = app_config['target']
model_name = app_config['model_name']


def predict(df):

    # Do custom processing
    common.preprocessing(df)

    try:
        df = requests.predict(model_name, df)
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return Response(f"Error model [{model_name}] not found. Has the model been trained and has it had enough time to start?")
        raise

    # Get calibration data from storage
    calibration_data = common.storage.get(common.get_calibration_data_storage_name(model.id))
    if calibration_data is None:
        raise Exception("No matching calibration data for UAT model.")

    # Calibrate
    superhuman_calibration.apply(
        df,
        calibration_data,
        in_place=True
    )

    df = common.postprocessing(df)

    return df
