import os
from . import data_node
import xxhash


class DataSourceFile(data_node.DataNode):

    def __init__(self, file_paths, data_source_name=None, **kwargs):
        if isinstance(file_paths, str):
            file_paths = (file_paths,)
        super().__init__(data_source_name)
        self.file_paths = file_paths
        self.kwargs = kwargs
        if data_source_name is None:
            if len(file_paths) == 1:
                base = os.path.basename(file_paths[0])
                self.data_source_name = os.path.splitext(base)[0]
            else:
                self.data_source_name = 'files'
        else:
            self.data_source_name = data_source_name

    def _read_file(self):
        files = []
        for fp in self.file_paths:
            with open(fp, 'r') as f:
                files.append(f.read())
        return files[0] if len(files) == 1 else files

    def _get_hash(self, data):
        x = xxhash.xxh64()
        x.update(self.data_source_name)
        for fp in self.file_paths:
            x.update(fp)
            x.update(str(os.path.getmtime(fp)))
        for k, v in self.kwargs.items():
            x.update(f"{k}: {str(v)}")
        return x.digest()

    def _execute(self, data):
        return {self.data_source_name: self._read_file()}
