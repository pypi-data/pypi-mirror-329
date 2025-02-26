
from . import data_node
import xxhash


class CustomNode(data_node.DataNode):

    def __init__(self, name, data_dependencies, *args):
        super().__init__(name)
        self.data_dependencies = data_dependencies
        self.args = args
        if isinstance(self.data_dependencies, str):
            self.data_dependencies = [self.data_dependencies]

    def _get_hash(self, data):
        x = xxhash.xxh64()
        for d in self.data_dependencies:
            x.update(data[d][1])
        for a in self.args:
            if a:
                x.update(str(a))
        return x.digest()