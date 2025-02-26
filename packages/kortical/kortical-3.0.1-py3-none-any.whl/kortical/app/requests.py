import logging
from multiprocessing import Pool
import pandas as pd
from tqdm import tqdm
from typing import Optional, Tuple
import kubernetes
import os

from kortical import api
from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.api.enums import ExplainProfile, ComponentType
from kortical.cloud.cloud import IS_KUBERNETES_ENVIRONMENT, is_beta_system

from kortical.helpers import str2enum


logger = logging.getLogger(__name__)
is_initialised = False
session = None

if IS_KUBERNETES_ENVIRONMENT:
    project = Project.get_selected_project()
    global_project_id = project.id
    global_environment_id = Environment.get_selected_environment(project).id
    # Disable debug logging from kubernetes package
    kubernetes.client.rest.logger.setLevel('WARNING')
    kubernetes.config.load_incluster_config()


def _init():
    global is_initialised
    global session
    if not is_initialised:
        api.init()
        session = api._api.session
        is_initialised = True


def _k8s_format(text):
    for char in [' ', '_']:
        text = text.replace(char, '-')
    return text.lower()


def _get_pod_webapp_port(pod_details: kubernetes.client.models.v1_pod.V1Pod) -> int:
    for container in pod_details.spec.containers:
        for port in container.ports:
            if port.name == 'webapp':
                return port.container_port
    raise Exception(f"No [webapp] port to use in pod [{pod_details.metadata.name}]")


def _get_designated_project_and_environment_ids(project_id: Optional[int] = None, environment_id: Optional[int] = None) -> Tuple:
    """Return the given project and environment ID if they are not None, otherwise returns the according global variable."""
    global global_project_id, global_environment_id
    if project_id is None:
        project_id = global_project_id
    if environment_id is None:
        environment_id = global_environment_id
    print(f"project_id {project_id}, environment_id {environment_id}")
    return project_id, environment_id


def _get_k8s_pod_urls(component_name: str, project_id: Optional[int], environment_id: Optional[int]):
    if not IS_KUBERNETES_ENVIRONMENT:
        raise Exception("Cannot use broadcast in a non-kubernetes environment.")
    project_id, environment_id = _get_designated_project_and_environment_ids(project_id, environment_id)
    project = api.project.Project.get_project(project_id)
    environment = api.environment.Environment.get_environment(project, environment_id)
    pod_list = kubernetes.client.CoreV1Api().list_namespaced_pod(
        os.environ.get('KORE_K8S_NAMESPACE'),
        label_selector=f"kore_project_name={_k8s_format(project.name)},kore_environment_name={_k8s_format(environment.name)},kore_component_name={_k8s_format(component_name)}"
    )
    component_webapp_port = _get_pod_webapp_port(pod_list.items[0])
    statefulset_name = pod_list.items[0].metadata.name[:-2]
    self_pod_name = os.environ.get('K8S_POD_NAME')
    return [
        f"http://{pod.metadata.name}.{statefulset_name}:{component_webapp_port}" for pod in pod_list.items if pod.metadata.name != self_pod_name
    ]

def _get_k8s_pod_full_url(pod_url: str, target_url: str):
    if target_url.startswith('/'):
        target_url = target_url[1:]
    return f"{pod_url}/{target_url}"

def _get_component_instance_url(
        component_name: str,
        component_type: ComponentType,
        url: str,
        project_id: Optional[int] = None,
        environment_id: Optional[int] = None
):
    if IS_KUBERNETES_ENVIRONMENT:
        project_id, environment_id = _get_designated_project_and_environment_ids(project_id, environment_id)
    else:
        if project_id is None:
            project = Project.get_selected_project(throw=False)
            if project is None:
                raise Exception("Please select a project, to see available projects you can run [kortical project list] on the command line and then [kortical project select <project-name-or-id>] to select one.")
            project_id = project.id
        if environment_id is None:
            environment = Environment.get_selected_environment(project, throw=False)
            if environment is None:
                raise Exception("Please select an environment, to see available environments you can run [kortical environment list] on the command line and then [kortical environment select <environment-name-or-id>] to select one.")
            environment_id = environment.id
    if url.startswith('/'):
        url = url[1:]

    component_type = str2enum(component_type, enum=ComponentType)

    return f"api/v1/projects/{project_id}/environments/{environment_id}/{component_type.value}s/{component_name}/{url}"


def _get_full_url(component_name: str,
                  component_type: ComponentType,
                  url: str,
                  project_id: Optional[int] = None,
                  environment_id: Optional[int] = None):

    component_instance_url = _get_component_instance_url(component_name, component_type, url, project_id, environment_id)
    url = f"{api.get_project_url()}{component_instance_url}"
    return url


def _starmap_kwargs_wrapper(function, arguments: list, keyword_arguments: dict):
    """Wrapper to give keyword arguments to a function called through starmap"""
    return function(*arguments, **keyword_arguments)


def _web_call(function_name,
              component_name: str,
              component_type: ComponentType,
              url: str,
              project_id: Optional = None,
              environment_id: Optional = None,
              broadcast: Optional = False,
              headers: Optional = {},
              *args,
              **kwargs):
    global session
    _init()
    if 'kortical_beta' not in headers and is_beta_system() is True:
        headers['kortical_beta'] = 'always'

    if broadcast is True:
        urls = _get_k8s_pod_urls(component_name, project_id, environment_id)
        keyword_arguments = kwargs
        keyword_arguments.update({
            'headers': headers
        })
        # Generate as many processes as available, spread the broadcast calls among them.
        # TODO - Make more processes than processors to avoid idling threads,
        #  since most of a process time is waiting for the remote server
        with Pool() as p:
            broadcast_responses = p.starmap(_starmap_kwargs_wrapper, [(
                # Get the appropriate session method
                getattr(session, function_name),
                # Pass the full url along with other positional arguments
                [f"{_get_k8s_pod_full_url(pod_url, url)}", *args],
                keyword_arguments
            ) for pod_url in urls])
        return broadcast_responses
    else:
        url = _get_full_url(component_name, component_type, url, project_id=project_id, environment_id=environment_id)
        return getattr(session, function_name)(url, headers=headers, **kwargs)


def get(component_name: str, component_type: ComponentType, url: str, params=None, project_id: Optional[int]=None, environment_id: Optional[int]=None, broadcast: Optional = False, **kwargs):
    return _web_call('get', component_name, component_type, url, params=params, project_id=project_id, environment_id=environment_id, broadcast=broadcast, **kwargs)


def put(component_name: str, component_type: ComponentType, url: str, data=None, project_id: Optional[int]=None, environment_id: Optional[int]=None, broadcast: Optional = False, **kwargs):
    return _web_call('put', component_name, component_type, url, data=data, project_id=project_id, environment_id=environment_id, broadcast=broadcast, **kwargs)


def head(component_name: str, component_type: ComponentType, url: str, project_id: Optional[int]=None, environment_id: Optional[int]=None, broadcast: Optional = False, **kwargs):
    return _web_call('head', component_name, component_type, url, project_id=project_id, environment_id=environment_id, broadcast=broadcast, **kwargs)


def post(component_name: str, component_type: ComponentType, url: str, data=None, json=None, project_id: Optional[int]=None, environment_id: Optional[int]=None, broadcast: Optional = False, **kwargs):
    return _web_call('post', component_name, component_type, url, data=data, json=json, project_id=project_id, environment_id=environment_id, broadcast=broadcast, **kwargs)


def patch(component_name: str, component_type: ComponentType, url: str, data=None, project_id: Optional[int]=None, environment_id: Optional[int]=None, broadcast: Optional = False, **kwargs):
    return _web_call('patch', component_name, component_type, url, data=data, project_id=project_id, environment_id=environment_id, broadcast=broadcast, **kwargs)


def delete(component_name: str, component_type: ComponentType, url: str, project_id: Optional[int]=None, environment_id: Optional[int]=None, broadcast: Optional = False, **kwargs):
    return _web_call('delete', component_name, component_type, url, project_id=project_id, environment_id=environment_id, broadcast=broadcast, **kwargs)


# Prediction
def predict(component_name: str,
            df: pd.DataFrame,
            explain_predictions: bool = False,
            explain_profile: ExplainProfile = ExplainProfile.ACCURATE,
            project_id: Optional[int] = None,
            environment_id: Optional[int] = None,
            **kwargs):

    explain_profile = str2enum(explain_profile, ExplainProfile)

    predict_url = f'/?flatten=true&explain_predictions={str(explain_predictions).lower()}&explain_profile={explain_profile.value}'
    model_instance_url = _get_component_instance_url(
        component_name,
        ComponentType.MODEL,
        predict_url,
        project_id=project_id,
        environment_id=environment_id
    )
    num_rows_per_batch = 2000
    df_out_batches = []
    number_of_batches = int(len(df) / num_rows_per_batch + 1)
    for i in tqdm(range(number_of_batches)):
        batch_size = min(num_rows_per_batch, len(df) - i * num_rows_per_batch)
        if batch_size > 0:
            start_index = i * num_rows_per_batch
            df_as_json = df[start_index:start_index + batch_size].to_json(orient='split')
            # Model components are our own code and we know what to expect, so we use api.post instead of the light
            # wrapper to benefit from auto login and error handling.
            response = api.post(
                model_instance_url,
                data=df_as_json,
                headers={'Content-Type': 'application/json', 'kortical_beta': 'always' if is_beta_system() else None}
            )

            logger.info(f"Validating predict response for batch {i + 1}/{number_of_batches}.")
            _check_and_parse_response(response)

            response_df = pd.read_json(response.text, orient='split', convert_dates=False, dtype=False)
            df_out_batches.append(response_df)

    df_out = pd.concat(df_out_batches)
    return df_out


def _check_and_parse_response(response):
    if response.headers['content-type'] == 'application/json':
        response_dict = response.json()
        if 'result' in response_dict and response_dict['result'] == 'error':
            raise Exception(f"{response.status_code} - {response_dict['message']}")
        else:
            return response_dict
    else:
        response.raise_for_status()
