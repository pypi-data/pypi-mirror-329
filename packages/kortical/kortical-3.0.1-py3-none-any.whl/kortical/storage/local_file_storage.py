import os
import shutil
import logging
import pickle
from pathlib import Path


from kortical.logging import logging_config
from kortical.storage.storage import Storage
from kortical.storage.helpers import DEFAULT_NAMESPACE, clean_namespace
from kortical.storage.storage_cache import StorageCache
from kortical.storage.exception import ItemExistsException, ItemNotFoundException, ItemNotWriteableException

logging_config.init_logger()
_logger = logging.getLogger(__name__)


class LocalFileStorage(Storage):
    def __init__(self, root_directory='kortical_storage_local_cache', app_name=None):
        self.root_directory = root_directory
        self.root_path = self.join_path(str(Path.home()), 'kortical', root_directory)
        self.cache = StorageCache(app_name)
        os.makedirs(self.root_path, exist_ok=True)

    @staticmethod
    def join_path(*paths):
        return os.path.join(*paths)

    @clean_namespace
    def store(self, name, item, namespace=DEFAULT_NAMESPACE, allow_overwrite=False):
        item_path = self.get_item_path(namespace, name)
        _logger.info(f'Writing item {self.join_path(namespace, name)} to path {item_path} and updating cache.')

        if os.path.isfile(item_path) and not allow_overwrite:
            message = f'File {self.join_path(namespace, name)} already exists. Specify "allow_overwrite=True" to overwrite'
            _logger.error(message)
            raise ItemExistsException(self, name, namespace)

        _logger.info(f'Writing item {self.join_path(namespace, name)} to {item_path}')
        try:
            self.write_item(item, item_path)
        except (TypeError, pickle.PicklingError) as e:
            if "can't pickle" in str(e).lower():
                _logger.error(f'Could not store item {self.join_path(namespace, name)} to {item_path} as it could not be serialized.')
            raise ItemNotWriteableException(self, name, namespace, item)

        self.cache.update(name, item, namespace)

    @clean_namespace
    def get(self, name, namespace=DEFAULT_NAMESPACE):
        _logger.info(f'Getting item {self.join_path(namespace, name)}...')

        if self.cache.contains(name, namespace):
            _logger.info(f'Found {self.join_path(namespace, name)} in cache.')
            return self.cache.get(name, namespace)

        item_path = self.get_item_path(namespace, name)

        if os.path.isfile(item_path):
            _logger.info(f'{self.join_path(namespace, name)} not in cache, Retrieving from filesystem.')
            with open(item_path, 'rb') as file:
                item = pickle.load(file)
                self.cache.update(name, item, namespace)
                return item
        else:
            _logger.error(f'File {self.join_path(namespace, name)} not found.')
            raise ItemNotFoundException(self, name, namespace)

    @clean_namespace
    def delete(self, name, namespace=DEFAULT_NAMESPACE):
        item_path = self.get_item_path(namespace, name)

        _logger.info(f'Deleting item {self.join_path(namespace, name)}')
        if os.path.isfile(item_path):
            self.cleanup_file(item_path)
        else:
            _logger.warning(f'item {self.join_path(namespace, name)} cannot be deleted from filesystem as it does not exist')
        if self.cache.contains(name, namespace):
            self.cache.delete(name, namespace)

    def list(self):
        def get_namespace_from_path(path):
            # What we need to remove from start of string, + 1 extra for the forward slash
            length_to_trim = len(self.root_path) + 1
            return path[length_to_trim:]

        items = set()
        directory_tree = list(os.walk(self.root_path))

        for root, dirs, files in directory_tree:
            namespace = get_namespace_from_path(root)
            if files:
                for file in files:
                    items.add(self.join_path(namespace, file))

        return list(items)

    def clear_storage(self):
        self.clear_cache()
        cache_items = os.listdir(self.root_path)
        if not cache_items:
            _logger.info(f'Local file storage is already empty')
        else:
            _logger.info(f'Deleting everything in local file storage')
            for root, dirs, files in os.walk(self.root_path):
                for name in files:
                    os.remove(self.join_path(root, name))
                for name in dirs:
                    shutil.rmtree(self.join_path(root, name))

    def clear_cache(self):
        _logger.info(f'Removing all items in cache')
        self.cache.purge()

    # when we delete a file in a namespace that suddenly becomes empty we want to delete all
    # other folders instead of having empty folders lying around with nothing in them
    def cleanup_file(self, path):
        os.remove(path)
        _current_directory, _ = os.path.split(path)
        while os.path.basename(os.path.normpath(_current_directory)) != self.root_directory:
            if len(os.listdir(_current_directory)) > 0:
                break
            os.rmdir(_current_directory)
            _current_directory, _ = os.path.split(_current_directory)

    def get_item_path(self, namespace, item_name):
        return self.join_path(self.root_path, namespace, item_name)

    @staticmethod
    def write_item(item, path):
        item_dir = os.path.dirname(path)
        created_namespace = False

        if not os.path.exists(item_dir):
            os.makedirs(item_dir)
            created_namespace = True

        try:
            with open(path, 'wb') as file:
                pickle.dump(item, file, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:
            # If that directory didn't exist before this failed write, we delete it
            if created_namespace:
                shutil.rmtree(item_dir)
            raise
