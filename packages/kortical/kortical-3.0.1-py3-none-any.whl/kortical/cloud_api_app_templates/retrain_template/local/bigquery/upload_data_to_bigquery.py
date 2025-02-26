import os
import pandas as pd

from module_placeholder.bigquery.bigquery import append_dataframe_to_bigquery
from module_placeholder.helpers.root_dir import from_root_dir

DATA_PATH = from_root_dir(os.path.join('data', 'dataset_1.csv'))

df = pd.read_csv(DATA_PATH)

append_dataframe_to_bigquery(df)
