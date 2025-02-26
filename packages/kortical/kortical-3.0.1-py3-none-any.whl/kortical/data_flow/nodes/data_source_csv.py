import pandas as pd
from . import data_source_file


class DataSourceCsv(data_source_file.DataSourceFile):

    def _read_file(self):
        files = []
        for fp in self.file_paths:
            files.append(pd.read_csv(fp, **self.kwargs))
        return files[0] if len(files) == 1 else files


