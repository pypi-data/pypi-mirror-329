from module_placeholder.constants import SELECTED_ENVIRONMENT, MODEL_NAME


class GetPredictionFromModel:

    def execute(self, data, progress_report_function):

        progress_report_function('Getting predictions...')

        df = data['df']

        model_instance = SELECTED_ENVIRONMENT.get_component_instance(MODEL_NAME)

        df_out = model_instance.predict(df)

        data['model_champion'] = model_instance
        data['df_out'] = df_out

        return data
