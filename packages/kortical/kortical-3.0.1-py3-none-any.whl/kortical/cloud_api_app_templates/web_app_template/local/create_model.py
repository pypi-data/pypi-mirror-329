import os
import pandas as pd

from kortical import api
from kortical.api.project import Project
from kortical.api.environment import Environment
from kortical.app import get_app_config

from module_placeholder.helpers.root_dir import from_root_dir

app_config = get_app_config(format='yaml')
data_file_name = app_config['data_file_name']
model_name = app_config['model_name']
target = app_config['target']

# To ensure the demo trains pretty quickly we:
#   - limit the solutions to linear models using TF-IDF and lemmatization
#   - Set random seeds
# Remove these restrictions for a full training run. To do this, simply remove the model code parameter, eg:
#   model = instance.train_model(
#       data,
#       number_of_train_workers=3,
#       target_score=0.97
#   )

model_code = """
- ml_solution:
  - data_set:
    - target_column: Category
    - problem_type: classification
    - evaluation_metric: f1_score
    - fraction_of_data_set_to_use: 1
    - cross_validation_folds: 3
    - data_set_random_seed: 1
    - modelling_random_seed: 1212414958
  - features:
    - numeric
    - categorical
    - text:
      - Text:
        - preprocessing:
          - custom:
            code: |
              @kortical.signature(input_columns=column_name, output_columns=[column_name, TEXT])
              def transform(column_name: str, input_columns: pd.DataFrame, fit_data):
                  lmtzr = nltk.stem.wordnet.WordNetLemmatizer()
                  column = input_columns[column_name].map(lambda x: ' '.join([lmtzr.lemmatize(word) for word in x.split()]))
                  return {column_name: column}

            remove_original_column: False
        - create_features:
          - tf-idf
    - date:
  - models:
    - linear"""


if __name__ == '__main__':
    api.init()

    project = Project.get_selected_project()
    environment = Environment.get_selected_environment(project)

    # Load dataset
    df = pd.read_csv(from_root_dir(os.path.join("data", data_file_name)))

    # Create and save train/test split
    df_train = df.sample(frac=0.8)
    df_test = df.drop(df_train.index)
    df_train.to_csv(from_root_dir(os.path.join("data", data_file_name.replace('.csv', '_train.csv'))), index=False)
    df_test.to_csv(from_root_dir(os.path.join("data", data_file_name.replace('.csv', '_test.csv'))), index=False)

    # Do custom pre-processing (data cleaning / feature creation)

    # Create model and train some model versions
    bbc_model = api.model.Model.create_or_select(model_name, delete_unpublished_versions=True, stop_train=True)
    data = api.data.Data.upload_df(df_train, name=model_name, targets=target)

    best_version = bbc_model.train_model(
        data,
        model_code=model_code,
        number_of_train_workers=3,
        target_score=0.965
    )

    print(f"Model score [{best_version.score} {best_version.score_type}]. Saving as default version...")
    bbc_model.set_default_version(best_version, wait_for_ready=False)

    print(f"Adding default version to environment [{environment}]...")
    environment.create_component_instance(model_name, wait_for_ready=True)

    print("Done.")
