from kortical.api.data import Data
from kortical.api.model import Model
from kortical.app import get_app_config

from module_placeholder.constants import SELECTED_ENVIRONMENT, MODEL_NAME

app_config = get_app_config(format='yaml')
target = app_config['target']

model_code = r"""- ml_solution:
  - data_set:
    - target_column: ['Account_Name']
    - problem_type: classification
    - evaluation_metric: f1_score
    - exclude_test_data_from_final_model: False
    - fraction_of_data_set_to_use: 1
    - fraction_of_data_to_use_as_test_set: 0.2
    - fix_test_set_boundary_when_downsampling: True
    - cross_validation_folds: 3
    - select_features: 1.0
    - shuffle_data_set: True
    - data_set_random_seed: 1
    - modelling_random_seed: 1520105539
  - features:
    - numeric
    - categorical
    - text:
      - Transaction
  - models:
    - lightgbm:
      - boosting_type: gbdt
      - subsample: 0.32
      - subsample_freq: 8
      - num_leaves: 197
      - max_depth: 5
      - class_weight: balanced
      - learning_rate: 0.44
      - n_estimators: 873
      - min_split_gain: 0.1
      - min_child_weight: 0.6934
      - min_child_samples: 6
      - colsample_bytree: 0.7000000000000001
      - reg_alpha: 0.189
      - reg_lambda: 0.711
      - max_bin: 171"""


class TrainModel:

    def execute(self, data, progress_report_function):

        df_train = data['df_train']

        progress_report_function('Uploading data to Kortical...')
        train_data = Data.upload_df(df_train, name=MODEL_NAME, targets=target)

        progress_report_function(f'Training model [{MODEL_NAME}]...')
        model = Model.create_or_select(MODEL_NAME, delete_unpublished_versions=True, stop_train=True)
        model_development = model.get_environment()

        best_retrained_version = model.train_model(
            train_data=train_data,
            model_code=model_code,
            number_of_train_workers=app_config.get('number_of_train_workers', 3),
            max_minutes_to_train=app_config.get('max_minutes_to_train', 10),
            max_models_with_no_score_change=app_config.get('max_models_with_no_score_change', 20)
        )

        progress_report_function(f'Best model score: {best_retrained_version.score} {best_retrained_version.score_type}')

        # Deploy
        model_challenger = model_development.create_component_instance(best_retrained_version.id, wait_for_ready=True)

        data['model'] = model
        data['model_challenger_version'] = best_retrained_version
        data['model_champion'] = SELECTED_ENVIRONMENT.get_component_instance(MODEL_NAME)
        data['model_challenger'] = model_challenger

        return data
