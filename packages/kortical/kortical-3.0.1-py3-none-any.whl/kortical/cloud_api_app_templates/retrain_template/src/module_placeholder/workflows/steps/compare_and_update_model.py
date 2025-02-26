from sklearn.metrics import f1_score
import time
from module_placeholder.constants import SELECTED_ENVIRONMENT

from kortical.app import get_app_config

app_config = get_app_config(format='yaml')
model_name = app_config['model_name']
target = app_config['target']


def _should_publish(challenger_score, champion_score):
    # Add extra requirements here.
    return challenger_score > champion_score


class CompareAndUpdateModel:

    def execute(self, data, progress_report_function):
        time.sleep(2)
        progress_report_function('Comparing newly trained model against existing model...')

        # Get model instances
        model = data['model']
        model_challenger_version = data['model_challenger_version']
        model_challenger = data['model_challenger']
        model_champion = data['model_champion']
        df_test = data['df_test']

        # Compare the performance of the challenger vs. champion model (i.e new vs. existing)
        challenger_predictions = model_challenger.predict(df_test)
        challenger_score = f1_score(challenger_predictions[target], challenger_predictions[f"predicted_{target}"],
                                    average='weighted')
        progress_report_function(f'challenger_score = [{challenger_score}]')

        if model_champion is None:
            should_publish = True
        else:
            champion_predictions = model_champion.predict(df_test)
            champion_score = f1_score(champion_predictions[target], champion_predictions[f"predicted_{target}"],
                                      average='weighted')
            progress_report_function(f'champion_score = [{champion_score}]')

            progress_report_function(f"New model score: [{challenger_score}], existing model score: [{champion_score}]")
            should_publish = _should_publish(challenger_score=challenger_score, champion_score=champion_score)

        # Deploy the new model
        if should_publish:
            model.set_default_version(model_challenger_version, wait_for_ready=False)
            progress_report_function(f"Deploying version [{model_challenger_version}] to environment [{SELECTED_ENVIRONMENT}]...")
            SELECTED_ENVIRONMENT.create_component_instance(model_challenger_version.id)
        else:
            progress_report_function(f"Not publishing, retrained version [{model.default_version.id}] has an inferior score to the existing version.")

        progress_report_function('Workflow complete.')

        return data
