import pytest
from kortical.app import get_app_config
from module_placeholder.api.http_status_codes import HTTP_OKAY, UNAUTHORISED

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']


@pytest.mark.api
def test_update_bigquery_endpoint(client):
    response = client.get(f'/update_bigquery?api_key={api_key}')
    assert response.status_code == HTTP_OKAY
    assert response.content_type == "text/html; charset=utf-8"


@pytest.mark.api
def test_update_bigquery_endpoint_no_api_key(client):
    response = client.get(f'/update_bigquery')
    assert response.status_code == UNAUTHORISED


@pytest.mark.api
def test_update_bigquery_endpoint_wrong_api_key(client):
    response = client.get(f'/update_bigquery?api_key={api_key}12345')
    assert response.status_code == UNAUTHORISED
