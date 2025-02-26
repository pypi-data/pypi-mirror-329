import pytest
import time
from kortical.api.enums import ComponentType
from kortical.app import get_app_config
from kortical.app import requests

from module_placeholder.api.http_status_codes import HTTP_OKAY


app_config = get_app_config(format='yaml')
api_key = app_config['api_key']
data_file_name = app_config['data_file_name']
model_name = app_config['model_name']
target = app_config['target']


def with_retries(function, *args, **kwargs):
    retries = 0
    while retries < 10:
        response = function(*args, **kwargs)
        if response.status_code in [200, 204]:
            return response
        time.sleep(0.5)
        retries += 1
    response.raise_for_status()


@pytest.mark.integration
@pytest.mark.smoke
def test_index():
    response = with_retries(requests.get, 'module_placeholder', ComponentType.APP, f'/?api_key={api_key}')
    assert response.status_code == HTTP_OKAY, response.text
    assert '<body' in response.text


@pytest.mark.integration
@pytest.mark.smoke
def test_predict_endpoint():
    response = with_retries(requests.post, 'module_placeholder', ComponentType.APP, f'/predict?api_key={api_key}', json={"input_text": "Here is some text"})
    assert response.status_code == HTTP_OKAY, response.text
