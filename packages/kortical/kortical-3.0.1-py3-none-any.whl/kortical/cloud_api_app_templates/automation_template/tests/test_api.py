import os
from io import BytesIO
import pandas as pd
import pytest
import requests
import tempfile
from kortical.app import get_app_config
from kortical.app import requests

from module_placeholder.workflows import common
from module_placeholder.api.http_status_codes import HTTP_OKAY
from tests.helpers import root_dir

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']
data_file_name = app_config['data_file_name']
app_url = f"{app_config['system_url']}/app/app_name_placeholder"


@pytest.mark.integration
def test_predict():
    df = pd.read_csv(root_dir.from_root_dir(os.path.join("data", data_file_name)))
    _, _, df_test = common.create_train_calibrate_and_test_datasets(df)
    with tempfile.NamedTemporaryFile('w+') as tmp:
        df_test.to_csv(tmp, index=False)
        tmp.flush()
        tmp.seek(0)
        response = requests.post(f'{app_url}/predict.csv?api_key={api_key}', files={'file': tmp})
    assert response.status_code == HTTP_OKAY
    df = pd.read_csv(BytesIO(response.content))
    df.head()


@pytest.mark.integration
def test_train():
    with open(root_dir.from_root_dir(os.path.join("data", data_file_name)), 'r') as f:
        response = requests.post(f'{app_url}/train?api_key={api_key}', files={'file': f})
    assert response.status_code == HTTP_OKAY


@pytest.mark.integration
def test_health():
    response = requests.get(f'{app_url}/health')
    assert response.status_code == HTTP_OKAY
    assert response.json() == {"result": "success"}
