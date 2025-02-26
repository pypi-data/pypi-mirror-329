import time
from datetime import datetime, timedelta

from kortical import api
from kortical.helpers.exceptions import KorticalKnownException, check_for_known_platform_errors


def list_projects(include_created_by=False):
    data = {
        'include_created_by': include_created_by
    }
    response = api.get('/api/v1/projects', params=data)
    return response.json()['projects']


def get_project(project_name_or_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}', throw=False)
    if response.status_code == 404:
        return None
    return response.json()['project']


def create_project(project_name, comma_separated_environment_names=None):
    data = {
        'name': project_name,
        'comma_separated_environment_names': comma_separated_environment_names
    }
    response = api.post('/api/v1/projects', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['project']


def delete_project(project_name_or_id):
    response = api.delete(f'/api/v1/projects/{project_name_or_id}')
    return response.json()


def get_project_kortical_config(project_name_or_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/kortical_config')
    kortical_config = response.json()['kortical_config']
    kortical_config_inherited = response.json()['kortical_config_inherited']
    return kortical_config, kortical_config_inherited


def set_project_kortical_config(project_name_or_id, kortical_config):
    response = api.patch(f'/api/v1/projects/{project_name_or_id}/kortical_config', json=kortical_config, throw=False)
    check_for_known_platform_errors(response)
    kortical_config = response.json()['kortical_config']
    kortical_config_inherited = response.json()['kortical_config_inherited']
    return kortical_config, kortical_config_inherited


def list_environments(project_name_or_id, include_created_by=False):
    data = {
        'include_created_by': include_created_by
    }
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments', params=data)
    return response.json()['environments']


def get_environment(project_name_or_id, environment_name_or_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}', throw=False)
    if response.status_code == 404:
        return None
    return response.json()['environment']


def get_environment_config(project_name_or_id, environment_name_or_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/config')
    return response.json()['environment_config']


def set_environment_config(project_name_or_id, environment_name_or_id, environment_config):
    data = {
        'config': environment_config
    }
    response = api.patch(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/config', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['environment_config']


def create_environment(project_name_or_id, environment_name, promotes_to_environment_name_or_id=None, component_config=None):
    data = {
        'name': environment_name,
        'component_config': component_config,
        'promotes_to_environment_name_or_id': promotes_to_environment_name_or_id
    }
    response = api.post(f'/api/v1/projects/{project_name_or_id}/environments', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['environment']


def delete_environment(project_name_or_id, environment_name_or_id):
    response = api.delete(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}', throw=False)
    if response.status_code not in [200, 400]:
        check_for_known_platform_errors(response)
    return response.json()


def promote_environment(project_name_or_id, environment_name_or_id):
    data = {
        'action_promote_environment': True
    }
    response = api.patch(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}', json=data)
    return response.json()['environment']


def list_challenger_environments(project_name_or_id, environment_name_or_id, user_email_or_id=None):
    data = {
        'user_email_or_id': user_email_or_id
    }
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/challengers', params=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['environments']


def create_challenger_environment(project_name_or_id, environment_name_or_id, challenger_name=None, component_config=None):
    data = {
        'challenger_name': challenger_name,
        'component_config': component_config
    }
    response = api.post(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/challengers', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['environment']


def get_environment_kortical_config(project_name_or_id, environment_name_or_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/kortical_config')
    kortical_config = response.json()['kortical_config']
    kortical_config_inherited = response.json()['kortical_config_inherited']
    return kortical_config, kortical_config_inherited


def set_environment_kortical_config(project_name_or_id, environment_name_or_id, kortical_config):
    response = api.patch(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/kortical_config', json=kortical_config, throw=False)
    check_for_known_platform_errors(response)
    kortical_config = response.json()['kortical_config']
    kortical_config_inherited = response.json()['kortical_config_inherited']
    return kortical_config, kortical_config_inherited


def list_component_instances(project_name_or_id, environment_name_or_id, include_created_by=False, include_deleted=False):
    data = {
        'include_created_by': include_created_by,
        'include_deleted': include_deleted
    }
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/components', params=data)
    return response.json()['component_instances']


def get_component_instance(project_name_or_id, environment_name_or_id, component_instance_id, component_type=None):
    params = None if component_type is None else {'component_type': component_type}
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/components/{component_instance_id}', params=params, throw=False)
    if response.status_code == 404:
        return None
    check_for_known_platform_errors(response)
    return response.json()['component_instance']


def create_component_instance(project_name_or_id, environment_name_or_id, component_name_or_version_id):
    data = {
        "component_name_or_version_id": component_name_or_version_id
    }
    response = api.post(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/components', json=data)
    return response.json()['component_instance']


def delete_component_instance(project_name_or_id, environment_name_or_id, component_name_or_instance_id):
    response = api.delete(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/components/{component_name_or_instance_id}')
    return response


def get_component_instance_kortical_config(project_name_or_id, environment_name_or_id, component_name_or_instance_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/components/{component_name_or_instance_id}/kortical_config')
    kortical_config = response.json()['kortical_config']
    kortical_config_inherited = response.json()['kortical_config_inherited']
    return kortical_config, kortical_config_inherited


def set_component_instance_kortical_config(project_name_or_id, environment_name_or_id, component_name_or_instance_id, kortical_config):
    response = api.patch(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/components/{component_name_or_instance_id}/kortical_config', json=kortical_config, throw=False)
    check_for_known_platform_errors(response)
    kortical_config = response.json()['kortical_config']
    kortical_config_inherited = response.json()['kortical_config_inherited']
    return kortical_config, kortical_config_inherited


def wait_for_component_instance_status(project_name_or_id, environment_name_or_id, component_instance_id, status, timeout_seconds=None, poll_frequency=1):
    if timeout_seconds is None:
        timeout_seconds = 180
    timeout_time = datetime.utcnow() + timedelta(seconds=timeout_seconds)
    while timeout_time > datetime.utcnow():
        component_instance = get_component_instance(project_name_or_id, environment_name_or_id, component_instance_id)
        if component_instance == None and status == 'Terminated':
            return
        if component_instance['status'] == status:
            return
        time.sleep(poll_frequency)
    raise KorticalKnownException(f"Timed out waiting for status [{status}] on component instance: project [{project_name_or_id}], environment [{environment_name_or_id}], component_instance_id [{component_instance_id}]")


def get_component_config(project_name_or_id, environment_name_or_id):
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/component_config')
    return response.json()['component_config']


def set_component_config(project_name_or_id, environment_name_or_id, component_config: str):
    data = {
        'component_config': component_config
    }
    response = api.patch(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/component_config', json=data, throw=False)
    check_for_known_platform_errors(response)
    return response.json()['environment']


def get_component_logs(project_name_or_id, environment_name_or_id, component_name_or_instance_id, replica=0):
    request_data = {
        'replica': replica
    }
    response = api.get(f'/api/v1/projects/{project_name_or_id}/environments/{environment_name_or_id}/components/{component_name_or_instance_id}/logs', json=request_data)
    return response.text
