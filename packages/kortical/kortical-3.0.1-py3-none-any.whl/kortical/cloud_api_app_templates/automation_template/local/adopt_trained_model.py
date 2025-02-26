import os
import pandas as pd
from kortical.app import get_app_config

from module_placeholder.workflows import superhuman_calibration, common

app_config = get_app_config(format='yaml')
data_file_name = app_config['data_file_name']

if __name__ == "__main__":
    df = pd.read_csv(os.path.join("..", "data", data_file_name))
    _, df_calibrate, df_test = common.create_train_calibrate_and_test_datasets(df)
    superhuman_calibration.superhuman_calibration(df_calibrate, df_test)
