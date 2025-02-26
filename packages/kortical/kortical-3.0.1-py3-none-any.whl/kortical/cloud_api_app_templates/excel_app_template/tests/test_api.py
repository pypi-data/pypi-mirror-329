import pytest
from kortical.app import get_app_config
from module_placeholder.api.http_status_codes import HTTP_OKAY, UNAUTHORISED

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']


@pytest.mark.api
def test_latest_churn_endpoint(client):
    response = client.get(f'/latest_churn.xlsx?api_key={api_key}')
    assert response.status_code == HTTP_OKAY
    assert response.content_type == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    assert len(response.data) > 0
    assert type(response.data) == bytes


@pytest.mark.api
def test_latest_churn_endpoint_no_api_key(client):
    response = client.get(f'/latest_churn.xlsx')
    assert response.status_code == UNAUTHORISED


@pytest.mark.api
def test_latest_churn_endpoint_wrong_api_key(client):
    response = client.get(f'/latest_churn.xlsx?api_key={api_key}12345')
    assert response.status_code == UNAUTHORISED
