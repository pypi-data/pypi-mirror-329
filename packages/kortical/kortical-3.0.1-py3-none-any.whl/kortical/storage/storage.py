from abc import ABC, abstractmethod

from kortical.storage.helpers import DEFAULT_NAMESPACE


class Storage(ABC):
    @staticmethod
    def join_path(*paths):
        raise NotImplementedError

    @abstractmethod
    def store(self, name, item, namespace=DEFAULT_NAMESPACE, allow_overwrite=False):
        raise NotImplementedError

    @abstractmethod
    def get(self, name, namespace=DEFAULT_NAMESPACE):
        raise NotImplementedError

    @abstractmethod
    def delete(self, name, namespace=DEFAULT_NAMESPACE):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError

    @abstractmethod
    def clear_storage(self):
        raise NotImplementedError

    @abstractmethod
    def clear_cache(self):
        raise NotImplementedError
