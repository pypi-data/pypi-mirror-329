
from . import transform
from . import data_node
from .. import stop_watch


class Report(transform.Transform):

    def _run(self, data, run_tests=True, cache_data=True):
        hash_value = self._hash_to_string(self._get_hash(data)) if cache_data else None

        with stop_watch.StopWatch(f'{self.name} execute'):
            output = self._execute(data)
        if output:
            new_output = {}
            for k, v in output.items():
                new_output[k] = [v, hash_value]
            output = new_output
        if hash_value and cache_data:
            data_node.data_cache.replace_and_store(self._hash, hash_value, output)
        self._hash = hash_value
        return output