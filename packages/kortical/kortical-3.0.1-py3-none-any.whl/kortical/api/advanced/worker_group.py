import re

from kortical import api
from kortical.helpers.exceptions import check_for_known_platform_errors, KorticalKnownException

# Worker group name pattern enforced by gcloud
WORKER_GROUP_NAME_PATTERN = re.compile(r'^(?:[a-z](?:[-a-z0-9]{0,38}[a-z0-9])?)$')


def list_worker_groups():
    response = api.get('/api/v1/worker_groups')
    return response.json()['worker_groups']


def create_worker_group(worker_group_name, worker_type, required_size):
    data = {
        'worker_group_name': worker_group_name,
        'worker_type': worker_type,
        'required_size': required_size
    }

    # Validate worker group name
    match = WORKER_GROUP_NAME_PATTERN.match(worker_group_name)

    if not match:
        raise KorticalKnownException(f'Cannot create worker group [{worker_group_name}]. Names can only '
                                     f'contain lower-case alphanumerics and "-", must start with a letter and end with an alphanumeric, '
                                     f'and must be no longer than 40 characters')

    response = api.post(f'/api/v1/worker_groups', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['worker_group']


def get_worker_group(worker_group_name_or_id):
    response = api.get(f'/api/v1/worker_groups/{worker_group_name_or_id}', throw=False)
    if response.status_code == 404:
        return None
    return response.json()['worker_group']


def update_worker_group(worker_group_name_or_id, required_size=None):
    data = {
        'required_size': required_size
    }
    response = api.patch(f'/api/v1/worker_groups/{worker_group_name_or_id}', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['worker_group']


def delete_worker_group(worker_group_name_or_id):
    response = api.delete(f'/api/v1/worker_groups/{worker_group_name_or_id}')
    return response.json()


def list_worker_types():
    response = api.get('/api/v1/worker_groups/worker_types')
    return response.json()['worker_types']


def get_default_worker_type():
    response = api.get('/api/v1/worker_groups/default_worker_type')
    return response.json()['default_worker_type']

