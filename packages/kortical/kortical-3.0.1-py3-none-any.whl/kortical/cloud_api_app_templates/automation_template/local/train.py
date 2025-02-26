import os
import pandas as pd
from module_placeholder.workflows import train, common
from kortical.app import get_app_config

app_config = get_app_config(format='yaml')
data_file_name = app_config['data_file_name']

if __name__ == "__main__":
    df = pd.read_csv(os.path.join("..", "data", data_file_name))
    df_train, df_calibrate, df_test = common.create_train_calibrate_and_test_datasets(df)
    train.train(df_train, df_calibrate, df_test)
