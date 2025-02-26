from functools import partial
import inspect
import xxhash
from . import data_node
from . import callable_tree
from ..wrapper import Wrapper


class Transform(data_node.DataNode):

    @staticmethod
    def get_transform_name(function):
        if isinstance(function, partial):
            return Transform.get_transform_name(function.func)
        elif callable(function) and hasattr(function, "__name__"):
            return function.__name__
        else:
            return "<unknown>"

    def __init__(self, name, transform_function):
        super().__init__(name)
        self.function = transform_function
        if isinstance(transform_function, Wrapper):
            self.parameter_names = transform_function.args
        else:
            self.parameter_names = list(inspect.signature(transform_function).parameters.keys())

    def _get_hash(self, data):
        x = xxhash.xxh64()
        for d in self.parameter_names:
            if not d in data:
                raise Exception(f"Function [{Transform.get_transform_name(self.function)}] requires [{d}] but it is not present in data.")
            x.update(data[d][1])
        ct = callable_tree.CallableTree(self.function, self.parameter_names)
        x.update(ct.get_hash())
        return x.digest()

    def _execute(self, data):
        return self.function(**{k: v[0] for k, v in data.items() if k in self.parameter_names})
