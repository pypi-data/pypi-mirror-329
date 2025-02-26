from kortical import api
from kortical.helpers.exceptions import check_for_known_platform_errors


def list_cronjobs(project_name_or_id, environment_name_or_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/cronjobs')
    return response.json()['cronjobs']


def create_cronjob(project_name_or_id, environment_name_or_id, cronjob_name, time_parameters, url, url_headers=None):
    data = {
        "name": cronjob_name,
        "time_parameters": time_parameters,
        "url": url,
        "url_headers": url_headers
    }
    response = api.post(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/cronjobs', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['cronjob']


def get_cronjob(project_name_or_id, environment_name_or_id, cronjob_name_or_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/cronjobs/{cronjob_name_or_id}', throw=False)
    if response.status_code == 404:
        return None
    check_for_known_platform_errors(response)
    return response.json()['cronjob']


def update_cronjob(project_name_or_id, environment_name_or_id, cronjob_name_or_id, time_parameters=None, url=None, url_headers=None):
    data = {
        'time_parameters': time_parameters,
        'url': url,
        'url_headers': url_headers
    }
    response = api.patch(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/cronjobs/{cronjob_name_or_id}', json=data)
    return response.json()['cronjob']


def delete_cronjob(project_name_or_id, environment_name_or_id, cronjob_name_or_id):
    response = api.delete(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/cronjobs/{cronjob_name_or_id}')
    return response
