import logging
import os
import pickle

from kortical import api
from kortical.cloud.cloud import IS_KUBERNETES_ENVIRONMENT
from kortical.logging import logging_config
from kortical.storage.storage import Storage
from kortical.storage.helpers import DEFAULT_NAMESPACE, clean_namespace
from kortical.storage.storage_cache import StorageCache
from kortical.storage.exception import ItemExistsException, ItemNotFoundException, ItemNotWriteableException

_HTTP_OKAY = 200
_HTTP_USER_INPUT_ERROR = 422
logging_config.init_logger()
_logger = logging.getLogger(__name__)


class PersistentCloudStorage(Storage):
    def __init__(self, app_name=None):
        if app_name is None and IS_KUBERNETES_ENVIRONMENT:
            app_name = os.environ['CLOUD_APP']

        self.app = app_name
        self.cache = StorageCache(app_name)

    @staticmethod
    def join_path(*paths):
        return "/".join(paths)

    def _send_item_to_cloud_storage(self, namespace, name, item, shared, allow_overwrite, timeout):
        request_args = {
            'namespace': namespace,
            'name': name,
            'overwrite': allow_overwrite
        }
        if shared:
            request_args['shared'] = shared
        else:
            request_args['app'] = self.app

        try:
            payload = pickle.dumps(item, protocol=pickle.HIGHEST_PROTOCOL)
        except (TypeError, pickle.PicklingError) as e:
            if "can't pickle" or '' in str(e).lower():
                _logger.error(f'Could not send item {self.join_path(namespace, name)} in Kortical cloud as it could not be serialized.')
            raise ItemNotWriteableException(self, name, namespace, item)

        api_url = '/api/v1/cloud/storage/blob'
        response = api.post(api_url, files={name: (name, payload)}, data=request_args, timeout=timeout, throw=False)

        if response.status_code != _HTTP_OKAY:
            _logger.error(f'API call to {api_url} returned HTTP status code of {response.status_code}.')

            error_message = response.text
            # If already exists (should not happen if 'overwrite' is True)
            if response.status_code == _HTTP_USER_INPUT_ERROR:
                _logger.info(f'Kortical Cloud returned error: {error_message}')

            if 'already exists in namespace' in error_message:
                raise ItemExistsException(self, name, namespace)

            raise Exception(f'Blob storage API request to Kortical Cloud failed. - {response.status_code}\n\n{error_message}')

    @clean_namespace
    def store(self, name, item, namespace=DEFAULT_NAMESPACE, shared=False, allow_overwrite=False, timeout=None):
        _logger.info(f'Storing item {"shared" if shared else self.app}:{self.join_path(namespace, name)} to cloud storage.')
        self._send_item_to_cloud_storage(namespace, name, item, shared, allow_overwrite, timeout)
        _logger.info(f'Successfully stored {"shared" if shared else self.app}:{self.join_path(namespace, name)} in Kortical Cloud')

        _logger.info(f'Updated item cache with {"shared" if shared else self.app}:{self.join_path(namespace, name)}')
        self.cache.update(name, item, namespace, shared)

    def _get_blob_from_cloud_storage(self, namespace, name, shared, timeout):
        request_args = {}
        if shared:
            request_args['shared'] = True
        else:
            request_args['app'] = self.app

        api_url = f'/api/v1/cloud/storage/blob/{namespace}/{name}'
        response = api.get(api_url, params=request_args, timeout=timeout, throw=False)
        if response.status_code == _HTTP_OKAY:
            return pickle.loads(response.content)
        else:
            if response.status_code == _HTTP_USER_INPUT_ERROR:
                error_message = response.text
                _logger.info(f'Kortical Cloud returned error: {error_message}')

                if 'not found' in error_message:
                    raise ItemNotFoundException(self, name, namespace)

            _logger.info(f'API call to {api_url} returned HTTP status code of {response.status_code}.')
            raise Exception('Blob retrieval API request to Kortical Cloud failed.')

    @clean_namespace
    def get(self, name, namespace=DEFAULT_NAMESPACE, shared=False, timeout=None):
        _logger.info(f'Retrieving item {"shared" if shared else self.app}:{namespace}/{name}')

        if self.cache.contains(name, namespace, shared):
            _logger.info(f'Found {"shared" if shared else self.app}:{self.join_path(namespace, name)} in cache')
            return self.cache.get(name, namespace, shared)

        _logger.info(f'Getting {"shared" if shared else self.app}:{self.join_path(namespace, name)} from Kortical Cloud')
        item = self._get_blob_from_cloud_storage(namespace, name, shared, timeout)
        self.cache.update(name, item, namespace, shared)
        return item

    def _delete_item_in_cloud_storage(self, name, namespace, shared, timeout):
        params = {}
        if shared:
            params['shared'] = shared
        else:
            params['app'] = self.app
        api_url = f'/api/v1/cloud/storage/blob/{namespace}/{name}'
        response = api.delete(api_url, params=params, timeout=timeout, throw=False)

        if response.status_code != _HTTP_OKAY:
            PersistentCloudStorage.raise_error_response(api_url, response.status_code)

    @clean_namespace
    def delete(self, name, namespace=DEFAULT_NAMESPACE, shared=False, timeout=None):
        _logger.info(f'Deleting {"shared" if shared else self.app}:{self.join_path(namespace, name)} from Kortical Cloud')

        self._delete_item_in_cloud_storage(name, namespace, shared, timeout)
        _logger.info(f'Successfully deleted {"shared" if shared else self.app}:{self.join_path(namespace, name)} from Kortical Cloud')

        self.cache.delete(name, namespace, shared)

    def list(self, app=False, shared=False, regex_filter=None, timeout=None):
        api_url = '/api/v1/cloud/storage/blob'

        # If user didn't specify, then we default to get both app and shared
        if not app and not shared:
            app = True
            shared = True

        request_data = {}
        if app:
            request_data['app'] = self.app
        if shared:
            request_data['shared'] = shared
        if regex_filter:
            request_data['regex_filter'] = regex_filter

        response = api.get(api_url, params=request_data, timeout=timeout, throw=False)
        if response.status_code != _HTTP_OKAY:
            PersistentCloudStorage.raise_error_response(api_url, response.status_code)

        response_data = response.json()
        return_data = {}
        if app:
            return_data['items'] = response_data.get('app', [])
        if shared:
            return_data['shared_items'] = response_data['shared']

        return return_data

    def clear_storage(self, timeout=None):
        _logger.info('Clearing persistent cloud file storage')
        self.clear_cache()

        api_url = f'/api/v1/cloud/storage/blob'
        response = api.delete(api_url, params={'app': self.app}, timeout=timeout, throw=False)

        if response.status_code != _HTTP_OKAY:
            PersistentCloudStorage.raise_error_response(api_url, response.status_code)

    def clear_cache(self):
        _logger.info(f'Removing all items in cache')
        self.cache.purge()

    @staticmethod
    def raise_error_response(api_url, status_code):
        _logger.error(f'API call to {api_url} returned HTTP status code of {status_code}.')
        raise Exception('API request to Kortical Cloud failed.')
