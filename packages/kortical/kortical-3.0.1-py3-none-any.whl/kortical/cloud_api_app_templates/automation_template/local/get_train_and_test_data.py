import os
import pandas as pd
from kortical.app import get_app_config

from module_placeholder.workflows import common


app_config = get_app_config(format='yaml')
data_file_name = app_config['data_file_name']

if __name__ == "__main__":
    df = pd.read_csv(os.path.join("..", "data", data_file_name))
    df_train, _, df_test = common.create_train_calibrate_and_test_datasets(df)
    df_train.to_csv(os.path.join("..", "data", data_file_name.lower().replace('.csv', '_train.csv')), index=False)
    df_test.to_csv(os.path.join("..", "data", data_file_name.lower().replace('.csv', '_test.csv')), index=False)
