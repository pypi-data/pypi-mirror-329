from . import data_node


class SaveCsv(data_node.DataNode):

    def __init__(self, name, file_path, data_source_name, **kwargs):
        super().__init__(name)
        self.file_path = file_path
        self.data_source_name = data_source_name
        self.kwargs = kwargs

    def _get_hash(self, data):
        return None

    def _execute(self, data):
        data[self.data_source_name][0].to_csv(self.file_path, index=False)
        return None
