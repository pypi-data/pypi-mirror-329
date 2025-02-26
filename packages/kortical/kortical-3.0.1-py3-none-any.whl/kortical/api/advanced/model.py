import time

from kortical import api
from kortical.helpers import print_warning
from kortical.helpers.exceptions import check_for_known_platform_errors, KorticalKnownException
from kortical.helpers.print_helpers import print_info, print_error, print_success


def list_models(include_created_by=False):
    data = {
        'include_created_by': include_created_by
    }
    response = api.get('/api/v1/models', params=data)
    return response.json()['models']


def get_model(model_name_or_id):
    response = api.get(f'/api/v1/models/{model_name_or_id}', throw=False)
    if response.status_code == 404:
        return None
    return response.json()['model']


def create_model(model_name):
    data = {'name': model_name}
    response = api.post('/api/v1/models', json=data, throw=False)
    check_for_known_platform_errors(response)
    models = list_models()
    while len([x for x in models if x['name'] == model_name and x['status'] == 'Running']) == 0:
        time.sleep(0.5)
        models = list_models()
    return response.json()['model']


def activate_model(model_name_or_id):
    response = api.patch(f'/api/v1/models/{model_name_or_id}', json={'active': True})
    return response.json()


def deactivate_model(model_name_or_id):
    response = api.patch(f'/api/v1/models/{model_name_or_id}', json={'active': False})
    return response.json()


def delete_model(model_name_or_id):
    response = api.delete(f'/api/v1/models/{model_name_or_id}', throw=False)
    check_for_known_platform_errors(response)

    # Wait for model to disappear from list
    models = list_models()
    while len([x for x in models if x['id'] == model_name_or_id]) > 0:
        time.sleep(0.5)
        models = list_models()


def select_model(model_name_or_id):
    model = get_model(model_name_or_id)
    if model is None:
        raise KorticalKnownException(f"Model [{model_name_or_id}] does not exist.")
    api.post(f'/api/v1/models/selected', json={'id': model['id']})


def delete_unpublished_versions(model_name_or_id):
    api.post(f'/api/v1/models/{model_name_or_id}/delete_unpublished_versions')


def list_model_versions(model_name_or_id, include_created_by=False):
    data = {
        'include_created_by': include_created_by
    }
    response = api.get(f'/api/v1/models/{model_name_or_id}/versions', params=data)
    return response.json()['model_versions']


def get_model_version(model_name_or_id, version_name_or_id):
    response = api.get(f'/api/v1/models/{model_name_or_id}/versions/{version_name_or_id}', throw=False)
    if response.status_code == 404:
        return None
    return response.json()['model_version']


def delete_model_version(model_name_or_id, version_name_or_id):
    response = api.delete(f'/api/v1/models/{model_name_or_id}/versions/{version_name_or_id}', throw=False)
    check_for_known_platform_errors(response)
    return response.json()


def set_default_model_version(model_name_or_id, version_name_or_id):
    data = {
        'action_make_default_version': True,
        'action_assign_version': True
    }
    response = api.patch(f'/api/v1/models/{model_name_or_id}/versions/{version_name_or_id}', json=data)
    return response.json()['model_version']


def set_model_version_description(model_name_or_id, version_name_or_id, description):
    data = {'description': description}
    response = api.patch(f'/api/v1/models/{model_name_or_id}/versions/{version_name_or_id}', json=data)
    return response.json()


def train_start(model_name_or_id, data_id, code):
    data = {'data_id': data_id, 'specification': code}
    response = api.post(f'/api/v1/models/{model_name_or_id}/train', data=data)
    return response.json()['run_id']


def train_stop(model_name_or_id):
    api.delete(f'/api/v1/models/{model_name_or_id}/train')


def train_status(model_name_or_id, number_of_models=10):
    params = {'number_of_models': number_of_models}
    response = api.get(f'/api/v1/models/{model_name_or_id}/train', params=params, timeout=30, throw=False)
    check_for_known_platform_errors(response)
    # TODO need to convert datetime back to datetime
    return response.json()


def wait_for_training(model_name_or_id, max_models_with_no_score_change=None, max_minutes_to_train=None, target_score=None):
    _train_status = train_status(model_name_or_id)

    if max_models_with_no_score_change is None and max_minutes_to_train is None and target_score is None:
        max_models_with_no_score_change = 50

    if not _train_status['is_training']:
        raise Exception(f"No training is occurring on model [{model_name_or_id}]. Please start training on this model first.")
    if max_minutes_to_train is not None:
        seconds_to_wait = max_minutes_to_train * 60
    else:
        seconds_to_wait = -1
    start_time = time.time()
    best_score = None
    beats_target_score = False

    while (max_models_with_no_score_change is None or _train_status['number_of_models_since_best_score'] < max_models_with_no_score_change) \
            and (max_minutes_to_train is None or (time.time() - start_time) < seconds_to_wait or best_score is None) \
            and not beats_target_score:
        print(f"Train status: score [{best_score}], score type [{_train_status['evaluation_metric']}], "
              f"number_of_models_since_best_score [{_train_status['number_of_models_since_best_score']}], "
              f"num_models_trained [{_train_status['num_models_trained']}], "
              f"num_train_workers [{_train_status['num_train_workers']}]")
        if _train_status['num_train_workers'] == 0:
            print_warning(f"Training is currently paused as there are no workers assigned to this model. "
                          f"Please log into the platform to assign workers to this model so training can resume.")
        time.sleep(5)
        _train_status = train_status(model_name_or_id)
        best_score = _train_status['top_models'][0]['score'] if len(_train_status['top_models']) > 0 else None
        if target_score is not None and best_score is not None:
            beats_target_score = best_score >= target_score if _train_status['is_maximising'] else best_score <= target_score

    print_success("Train stopping condition reached")
    train_stop(model_name_or_id)

    return _train_status


def set_num_train_workers(model_name_or_id, number_of_train_workers):
    data = {'required_worker_count': number_of_train_workers}
    response = api.patch(f'/api/v1/models/{model_name_or_id}/train', data=data, throw=False)
    if response.status_code not in [200, 204]:
        print_error(f"Failed to set number of workers to [{number_of_train_workers}]. Please log into the platform "
                    f"to see what else is training and free up enough workers.")
    else:
        print_info(f"Number of workers set to [{number_of_train_workers}].")
