from sklearn.metrics import f1_score
from kortical import api
from kortical.app import get_app_config
from module_placeholder.workflows import common, superhuman_calibration

app_config = get_app_config(format='yaml')
target = app_config['target']
target_accuracy = app_config['target_accuracy']
model_name = app_config['model_name']


def train(df_train, df_calibrate, df_test):
    api.init(app_config['system_url'])

    # Do custom processing
    datasets = [df_train]
    for df in datasets:
        common.preprocessing(df)

    # Create model
    instance = api.instance.Model.create_or_select(model_name, delete_unpublished_models=True, stop_train=True)
    data = api.data.Data.upload_df(df_train, name=model_name)
    data.set_targets(target)

    model = instance.train_model(
        data,
        model_code=common.model_code,
        number_of_train_workers=6,
        # Remove this minutes limitation to run in production and produce better models
        max_minutes_to_train=2,
        max_models_with_no_score_change=50
    )

    model.publish('Integration')
    superhuman_calibration.superhuman_calibration(df_calibrate, df_test)

