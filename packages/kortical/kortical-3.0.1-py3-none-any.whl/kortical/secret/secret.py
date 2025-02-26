from kortical import api
from kortical.helpers.exceptions import check_for_known_platform_errors


def set(key, value, overwrite=False):
    request_data = {'key': key,
                    'value': value,
                    'overwrite': overwrite}
    response = api.post('/api/v1/secrets', params=request_data, throw=False)
    check_for_known_platform_errors(response)
    response = response.json()
    return response


def get(key):
    response = api.get('/api/v1/secrets', params={'key': key})
    response = response.json()
    return response['value']


def delete(key):
    response = api.delete('/api/v1/secrets', params={'key': key})
    response = response.json()
    return response
