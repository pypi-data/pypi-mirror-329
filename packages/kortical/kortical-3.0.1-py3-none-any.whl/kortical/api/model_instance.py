from datetime import datetime
import pandas as pd

from kortical.api.component_instance import ComponentInstance
from kortical.api.enums import ExplainProfile, ComponentType


class ModelInstance(ComponentInstance):

    @classmethod
    def _create_from_json(cls, project_id, environment_id, component_instance_json):
        created = datetime.strptime(component_instance_json['created']['__value__'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        return cls(
            id_=component_instance_json['id'],
            name=component_instance_json['name'],
            type_=component_instance_json['type'],
            created=created,
            created_by=component_instance_json.get('created_by'),
            status=component_instance_json['status'],
            project=project_id,
            environment=environment_id,
            component_id=component_instance_json['component_id'],
            component_version_id=component_instance_json['component_version_id'],
            kubernetes_name=component_instance_json['kubernetes_name']
        )

    @classmethod
    def list(cls, project, environment, include_created_by=False, include_deleted=False):
        return ComponentInstance.list(project, environment, ComponentType.MODEL, include_created_by=include_created_by, include_deleted=include_deleted)

    @classmethod
    def create_model_instance(cls, project, environment, model_name_or_version_id, wait_for_ready=False):
        model_instance = ComponentInstance.create_component_instance(project, environment, model_name_or_version_id, wait_for_ready)
        return model_instance

    @classmethod
    def get_model_instance(cls, project, environment, model_name_or_instance_id):
        model_instance = ComponentInstance.get_component_instance(project, environment, model_name_or_instance_id, component_type=ComponentType.MODEL)
        return model_instance

    def get_model_version(self):
        from kortical.api.model import Model
        from kortical.api.model_version import ModelVersion

        model = Model.get_model(self.component_id)
        model_version = ModelVersion.get_version(model, self.version_id)
        return model_version

    def get_model(self):
        from kortical.api.model import Model

        model = Model.get_model(self.component_id)
        return model

    def predict(self,
                df: pd.DataFrame,
                explain_predictions: bool = False,
                explain_profile: ExplainProfile = ExplainProfile.ACCURATE,
                **kwargs):
        from kortical.app import requests
        df_out = requests.predict(component_name=self.name,
                                  df=df,
                                  explain_predictions=explain_predictions,
                                  explain_profile=explain_profile,
                                  project_id=self.project.id,
                                  environment_id=self.environment.id,
                                  **kwargs)
        return df_out
