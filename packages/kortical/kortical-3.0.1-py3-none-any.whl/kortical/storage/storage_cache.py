import logging
from copy import deepcopy

from kortical.logging import logging_config

logging_config.init_logger()
_logger = logging.getLogger(__name__)


class StorageCache:

    def __init__(self, app):
        self._cache = {}
        self.app = app

    def update(self, name, item, namespace, shared=False):
        _logger.info(f'Updating cache with {namespace}/{name}')
        self._cache[self._get_key(name, namespace, shared)] = deepcopy(item)

    def get(self, name, namespace, shared=False):
        try:
            return deepcopy(self._cache[self._get_key(name, namespace, shared)])
        except KeyError:
            _logger.error(f'Item with name {"shared" if shared else self.app}:{namespace}/{name}] not found in blob cache.')
            raise

    def contains(self, name, namespace, shared=False):
        return self._get_key(name, namespace, shared) in self._cache

    def delete(self, name, namespace, shared=False):
        _logger.info(f'Deleting item {"shared" if shared else self.app}:{namespace}/{name}')
        try:
            del self._cache[self._get_key(name, namespace, shared)]
        except KeyError:
            _logger.info(f'Item {"shared" if shared else self.app}:{namespace}/{name} already not in cache.')

    def purge(self):
        self._cache.clear()

    def __len__(self):
        return len(self._cache)

    def _get_key(self, name, namespace, shared):
        if shared:
            return name, namespace, 'shared'
        else:
            return name, namespace, self.app
