import datetime
import os
import tempfile
from io import BytesIO

import pandas as pd
import pytest
from time import sleep

from kortical.api.enums import ComponentType
from kortical.app import get_app_config
from kortical.app import requests

from module_placeholder.constants import SELECTED_ENVIRONMENT, MODEL_NAME
from module_placeholder.api.http_status_codes import HTTP_OKAY
from module_placeholder.helpers import root_dir

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']

"""
    Simple integration tests that check the train and predict workflows.
"""


@pytest.mark.api
def test_train_workflow():
    old_model_instance = SELECTED_ENVIRONMENT.get_component_instance(MODEL_NAME)

    response = requests.post('module_placeholder', component_type=ComponentType.APP, url=f'/train?api_key={api_key}')
    assert response.status_code == HTTP_OKAY
    train_id = response.json()['train_id']

    start_time = datetime.datetime.utcnow()
    status = ''
    while 'complete' not in status:
        if datetime.datetime.utcnow() - start_time > datetime.timedelta(minutes=30):
            raise Exception("Timed out.")

        response = requests.get('module_placeholder', component_type=ComponentType.APP, url=f'/train/{train_id}?api_key={api_key}')
        assert response.status_code == HTTP_OKAY
        print(response.json())
        status = response.json()['status']
        sleep(1)

    new_model_instance = SELECTED_ENVIRONMENT.get_component_instance(MODEL_NAME)
    assert new_model_instance.version.id >= old_model_instance.version.id


@pytest.mark.api
@pytest.mark.smoke
def test_predict_workflow():

    df = pd.read_csv(root_dir.from_root_dir(os.path.join("data", 'dataset_2.csv')))

    with tempfile.NamedTemporaryFile('w+') as tmp:
        df.to_csv(tmp, index=False)
        tmp.flush()
        tmp.seek(0)
        response = requests.post('module_placeholder', component_type=ComponentType.APP,
                                 url=f'/predict?api_key={api_key}',
                                 files={'file': tmp})

    assert response.status_code == HTTP_OKAY
    df = pd.read_csv(BytesIO(response.content))
    df.head()
