from kortical import api
from kortical.helpers.exceptions import check_for_known_platform_errors


def list_apps():
    response = api.get('/api/v1/apps')
    return response.json()['apps']


def get_app(app_name_or_id):
    response = api.get(f'/api/v1/apps/{app_name_or_id}', throw=False)
    if response.status_code == 404:
        return None
    return response.json()['app']


def create_app(app_name):
    data = {'name': app_name}
    response = api.post('/api/v1/apps', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['app']


def delete_app(app_name_or_id):
    response = api.delete(f'/api/v1/apps/{app_name_or_id}', throw=False)
    check_for_known_platform_errors(response)
    return response.json()


def list_app_versions(app_name_or_id, include_created_by=False):
    data = {
        'include_created_by': include_created_by
    }
    response = api.get(f'/api/v1/apps/{app_name_or_id}/versions', params=data)
    return response.json()['app_versions']


def get_app_version(app_name_or_id, version_name_or_id):
    response = api.get(f'/api/v1/apps/{app_name_or_id}/versions/{version_name_or_id}', throw=False)
    if response.status_code == 404:
        return None
    return response.json()['app_version']


def delete_app_version(app_name_or_id, version_name_or_id):
    response = api.delete(f'/api/v1/apps/{app_name_or_id}/versions/{version_name_or_id}', throw=False)
    check_for_known_platform_errors(response)
    return response.json()


def get_app_version_config(app_name_or_id, version_name_or_id):
    response = api.get(f'/api/v1/apps/{app_name_or_id}/versions/{version_name_or_id}/config')
    return response.json()['app_config']


def set_app_version_config(app_name_or_id, version_name_or_id, app_config):
    data = {
        'config': app_config
    }
    response = api.patch(f'/api/v1/apps/{app_name_or_id}/versions/{version_name_or_id}/config', json=data)
    return response.json()['app_config']


def set_app_version_description(app_name_or_id, version_name_or_id, description):
    data = {'description': description}
    response = api.patch(f'/api/v1/apps/{app_name_or_id}/versions/{version_name_or_id}', json=data)
    return response.json()


def restart_app_instance(project_name_or_id, environment_name_or_id, component_name_or_instance_id):
    response = api.post(
        f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/apps/{component_name_or_instance_id}/restart',
        throw=False
    )
    check_for_known_platform_errors(response)
    return response.json()


def get_app_config(project_name_or_id, environment_name_or_id, component_name_or_instance_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/apps/{component_name_or_instance_id}/config')
    return response.json()['app_config']


def set_app_config(project_name_or_id, environment_name_or_id, component_name_or_instance_id, app_config, restart=True):
    data = {
        'config': app_config,
        'restart_app_instance': restart
    }
    response = api.patch(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/apps/{component_name_or_instance_id}/config', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['app_config']


def create_app_version(app_name_or_id, k8s_config, app_config=None):
    data = {
        'k8s_config': k8s_config,
        'app_config': app_config
    }
    response = api.post(f'/api/v1/apps/{app_name_or_id}/versions', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['app_version']


def set_default_app_version(app_name_or_id, version_name_or_id):
    data = {
        'action_make_default_version': True,
        'action_assign_version': True
    }
    response = api.patch(f'/api/v1/apps/{app_name_or_id}/versions/{version_name_or_id}', json=data)
    return response.json()['app_version']
