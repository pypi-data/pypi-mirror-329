import os
import pandas as pd
import pytest
from kortical.app import get_app_config

from module_placeholder.api.http_status_codes import HTTP_OKAY, UNAUTHORISED

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']


@pytest.mark.unit
def test_index_endpoint(client):
    response = client.get(f'/?api_key={api_key}')
    assert response.status_code == HTTP_OKAY


@pytest.mark.unit
def test_chat_endpoint(client):
    response = client.post(f'/chat?api_key={api_key}', json={"conversation": [{"role": "user", "content": "Who are you?"}]})
    assert response.status_code == HTTP_OKAY, response.text


@pytest.mark.unit
def test_chat_endpoint_no_api_key(client):
    response = client.post(f'/chat')
    assert response.status_code == UNAUTHORISED


@pytest.mark.unit
def test_chat_endpoint_wrong_api_key(client):
    response = client.post(f'/chat?api_key={api_key}12345')
    assert response.status_code == UNAUTHORISED
