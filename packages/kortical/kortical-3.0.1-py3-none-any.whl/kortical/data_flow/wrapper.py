
class Wrapper:

    def __init__(self, function, inputs_map={}, outputs_map={}):
        self.function = function
        self.inputs_map = inputs_map
        self.outputs_map = outputs_map

    def __call__(self, **kwargs):
        kwargs = {k if k not in self.inputs_map else self.inputs_map[k]: v for k, v in kwargs.items()}
        output = self.function(**kwargs)
        if output is not None and not isinstance(output, dict):
            raise Exception(f"Please ensure that [{self.function.__name__}] returns a dictionary in the format data_name: data_value")
        output = {k if k not in self.outputs_map else self.outputs_map[k]: v for k, v in output.items()}
        return output

    @property
    def args(self):
        return list(self.inputs_map.keys())

    @property
    def func(self):
        return self.function