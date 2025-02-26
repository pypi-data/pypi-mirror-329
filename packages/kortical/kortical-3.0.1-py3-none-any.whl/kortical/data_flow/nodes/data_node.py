import xxhash
import base64
from .. import data_cache
from .. import stop_watch


data_cache_folder = '.kore_data_cache'
data_cache = data_cache.DataCache(data_cache_folder)


class DataNode(object):

    def __init__(self, name):
        self.name = name
        self._hash = None
        self._parents = []
        self._children = []
        self._output = None
        self._tests = []

    def add_child(self, child):
        self._children.append(child)
        child._parents.append(self)
        return child

    def add_parents(self, parents):
        for p in parents:
            p.add_child(self)
        return self

    @staticmethod
    def _hash_data(data):
        x = xxhash.xxh64()
        x.update(data)
        return x.digest()

    def _hash_to_string(self, hash_value):
        return base64.b64encode(hash_value).decode() if hash_value is not None else None

    def _run(self, data, run_tests=True, cache_data=True):
        if cache_data:
            hash_value = self._hash_to_string(self._get_hash(data))
            if hash_value:
                output = data_cache.fetch(hash_value)
            else:
                output = None
        else:
            output = None
            hash_value = None

        if output is None:
            with stop_watch.StopWatch(f'{self.name} execute'):
                output = self._execute(data)
                if output is not None and not isinstance(output, dict):
                    raise Exception(f"Please ensure that [{self.name}] returns a dictionary in the format data_name: data_value")

            # run tests
            if run_tests and len(self._tests) > 0:
                test_data = data.copy()
                test_data.update({k: [v, None] for k, v in output.items()})
                print(f"About to run [{len(self._tests)}] tests")
                for test in self._tests:
                    test._execute(test_data)
                    print(f"Test [{test.name}] successful")
            if output:
                new_output = {}
                for k, v in output.items():
                    new_output[k] = [v, hash_value]
                output = new_output
            if hash_value and cache_data:
                data_cache.replace_and_store(self._hash, hash_value, output)

            self._hash = hash_value
        return output