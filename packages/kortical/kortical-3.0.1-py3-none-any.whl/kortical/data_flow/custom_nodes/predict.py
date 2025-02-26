import time

import pandas as pd
from tqdm import tqdm

from kortical import api
from kortical.api.advanced import model
from kortical.data_flow.nodes import custom_node


class Predict(custom_node.CustomNode):

    def __init__(self, kortical_url, data_source, model_id=None, instance_name=None, deployment_name=None, name=None):
        super().__init__(f"{data_source}_predict" if name is None else name, ['model_id', 'instance_name', 'deployment_name'], model_id, instance_name, deployment_name)
        self.url = kortical_url
        self.data_source = data_source
        self.model_id = model_id
        self.instance_name = instance_name
        self.deployment_name = deployment_name

        api.init(self.url)

    def url_transfrom(self, text):
        return text.lower().replace(' ', '_')

    def _execute(self, data):
        df_in = data[self.data_source][0]
        if not self.instance_name:
            if 'instance_name' not in data:
                raise Exception('Please pass in an "instance_name" argument to the predict node, with the name of the model instance to predict against.')
            instance_name = self.url_transfrom(data['instance_name'][0])
        else:
            instance_name = self.instance_name

        if not self.deployment_name:
            if 'deployment_name' not in data:
                raise Exception('Please pass in an "deployment_name" argument to the predict node, with the name of the deployment to predict against. eg: deployment_name="Integration"')
            deployment_name = self.url_transfrom(data['deployment_name'][0])
        else:
            deployment_name = self.deployment_name
        predict_url = f'/api/v1/{instance_name}/predict/{deployment_name}?flatten=true&explain_predictions=false&explain_profile=none'

        model.select_model(instance_name)
        time.sleep(10)
        df_out = self._kortical_predict(predict_url, df_in)

        return {self.data_source: df_out, 'instance_name': instance_name, 'deployment_name': deployment_name}

    @staticmethod
    def _kortical_predict(predict_url, df_in, drop_index_columns=True):
        num_rows_per_batch = 2000
        df_in = df_in.reset_index(drop=drop_index_columns)

        df_out_batches = []

        for i in tqdm(range(int(df_in.shape[0] / num_rows_per_batch + 1))):
            batch_size = min(num_rows_per_batch, df_in.shape[0] - i*num_rows_per_batch)
            if batch_size > 0:
                df_as_json = df_in[i*num_rows_per_batch:i*num_rows_per_batch+num_rows_per_batch].to_json(orient='split')
                response = api.post(predict_url, data=df_as_json, headers={'Content-Type': 'application/json'})
                if response.status_code != 200:
                    raise Exception(f"Predict error: {response.json()['message']}")
                response_df = pd.read_json(response.text, orient='split', convert_dates=False, dtype=False)
                df_out_batches.append(response_df)

        df_out = pd.concat(df_out_batches)
        return df_out