import kortical.api.advanced.data
import kortical.api.advanced.model
from kortical.data_flow.nodes import custom_node
from kortical import api
from kortical.api import advanced


class Model(custom_node.CustomNode):

    def __init__(self, kortical_url, data_source_train, model_code=None, targets=None, number_of_train_workers=None, minutes_to_train=60, max_models_with_no_score_change=200, name=None):
        super().__init__(name if name is not None else f"{data_source_train}_model", data_source_train, model_code, targets, minutes_to_train, max_models_with_no_score_change, name)
        self.url = kortical_url
        self.data_source_train = data_source_train
        self.model_code = model_code
        self.targets = targets
        self.number_of_train_workers = number_of_train_workers
        self.minutes_to_train = minutes_to_train
        self.max_models_with_no_score_change = max_models_with_no_score_change

    def _execute(self, data):
        instance_name = self.name
        df = data[self.data_source_train][0]
        train_data = bytes(df.to_csv(index=False), encoding='utf-8')
        api.init(self.url)
        instances = advanced.model.list_models()
        instance = [x for x in instances if x['name'] == instance_name]
        if len(instance) > 0:
            instance = instance[0]
            advanced.model.delete_unpublished_versions(instance['id'])
            kortical.api.advanced.model.train_stop(instance['id'])
        else:
            instance = advanced.model.create_model(instance_name)
        advanced.model.select_model(instance['id'])

        # Stop a train run if a train is already in progress
        train_status = kortical.api.advanced.model.train_status(instance['id'])
        if train_status['is_training']:
            kortical.api.advanced.model.train_stop(instance['id'])

        data_id = advanced.data.upload_data(self.data_source_train, train_data)
        if self.targets:
            api.data.set_targets(data_id, self.targets)
        if self.model_code is None:
            code = kortical.api.advanced.data.generate_code(data_id)
        else:
            errors = kortical.api.advanced.data.validate_code(data_id, self.model_code)
            if len(errors) > 0:
                raise Exception(f"Model code validation failed, please fix the model_code\n\n{errors}")
            code = self.model_code

        train_id = kortical.api.advanced.model.train_start(instance['id'], data_id, code)

        if self.number_of_train_workers:
            kortical.api.advanced.model.set_num_train_workers(instance['id'], self.number_of_train_workers)

        train_status = kortical.api.advanced.model.wait_for_training(instance['id'], self.max_models_with_no_score_change, self.minutes_to_train)
        best_model_id = train_status['top_models'][0]['id']

        deployments = advanced.model.list_deployments(instance['id'])
        deployment = 'Integration'
        deployment_id = [x for x in deployments if x['name'] == deployment][0]['id']

        advanced.model.publish_model(deployment_id, best_model_id)
        advanced.model.wait_for_live_model(instance_name, deployment, best_model_id)

        return {
            'instance_id': instance['id'],
            'instance_name': instance_name,
            'model_id': best_model_id,
            'model_score': train_status['top_models'][0]['score'],
            'evaluation_metric': train_status['evaluation_metric'],
            'targets': self.targets,
            'deployment_name': deployment
        }
