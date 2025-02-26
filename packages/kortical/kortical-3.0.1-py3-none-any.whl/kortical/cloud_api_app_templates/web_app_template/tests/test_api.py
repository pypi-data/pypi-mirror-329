import os
import pandas as pd
import pytest
from kortical.app import get_app_config
from kortical.app import requests

from module_placeholder.helpers.root_dir import from_root_dir
from module_placeholder.api.http_status_codes import HTTP_OKAY, UNAUTHORISED

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']
data_file_name = app_config['data_file_name']
model_name = app_config['model_name']
target = app_config['target']


@pytest.mark.unit
def test_index_endpoint(client):
    response = client.get(f'/?api_key={api_key}')
    assert response.status_code == HTTP_OKAY


@pytest.mark.unit
def test_predict_endpoint(client):
    response = client.post(f'/predict?api_key={api_key}', json={"input_text": "Here is some text"})
    assert response.status_code == HTTP_OKAY, response.text


@pytest.mark.unit
def test_predict_endpoint_no_api_key(client):
    response = client.post(f'/predict')
    assert response.status_code == UNAUTHORISED


@pytest.mark.unit
def test_predict_endpoint_wrong_api_key(client):
    response = client.post(f'/predict?api_key={api_key}12345')
    assert response.status_code == UNAUTHORISED


@pytest.mark.unit
def test_model_accuracy(client):
    # Calculate an end-to-end score, including pre/post-processing (sends predicts to the model through the app)
    test_set_path = from_root_dir(os.path.join("data", data_file_name.replace('.csv', '_test.csv')))
    df = pd.read_csv(test_set_path)

    request_data = {"input_text": list(df['Text'])}

    response = client.post(f'/predict?api_key={api_key}', json=request_data)
    assert response.status_code == HTTP_OKAY

    df[f'predicted_{target}'] = [x.decode() for x in response.response]
    correct_predictions = df.loc[df[f'predicted_{target}'] == df[target]]
    accuracy = len(correct_predictions) / len(df)

    print(f"Accuracy is [{accuracy}]")
    assert accuracy > 0.95
