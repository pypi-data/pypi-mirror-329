from typing import Optional
import urllib.parse

from kortical.api import advanced
from kortical.api.enums import ComponentInstanceState, ComponentType
from kortical.api.model_version import ModelVersion
from kortical.api.app_version import AppVersion
from kortical.config import kortical_config

from kortical.helpers import str2enum
from kortical.helpers.print_helpers import print_info


class ComponentInstance:

    @classmethod
    def create_component_instance(cls, project, environment, component_name_or_version_id, wait_for_ready=False):
        component_instance_json = advanced.project.create_component_instance(project.id, environment.id, component_name_or_version_id)
        component_instance = cls._create_from_json(project, environment, component_instance_json)
        if wait_for_ready:
            component_instance.wait_for_status(ComponentInstanceState.RUNNING)
        return component_instance

    @classmethod
    def list(cls, project, environment, component_type: Optional[ComponentType] = None, include_created_by=False, include_deleted=False):
        component_type = str2enum(component_type, enum=ComponentType)
        component_instances_json = advanced.project.list_component_instances(project.id, environment.id, include_created_by, include_deleted)
        component_instances = [cls._create_from_json(project, environment, x) for x in component_instances_json]
        if component_type is not None:
            component_instances = [c for c in component_instances if c.type == component_type]
        return component_instances

    @classmethod
    def get_component_instance(cls, project, environment, component_name_or_instance_id, component_type: Optional[ComponentType] = None):
        component_type = str2enum(component_type, enum=ComponentType).value if component_type else None
        component_instance_json = advanced.project.get_component_instance(project.id, environment.id, component_name_or_instance_id, component_type)
        component_instance = cls._create_from_json(project, environment, component_instance_json)
        return component_instance

    def __init__(self, project, environment, id_, name, type_, status, created, component_version_id, component_id, kubernetes_name, created_by=None):
        self.id = id_
        self.name = name
        if type_ == 'model':
            model_version_json = advanced.model.get_model_version(component_id, component_version_id)
            version = ModelVersion._create_from_json(model_version_json)
        elif type_ == 'app':
            app_version_json = advanced.app.get_app_version(component_id, component_version_id)
            version = AppVersion._create_from_json(app_version_json)
        else:
            raise Exception("Invalid component type.")
        self.version = version
        self.type = ComponentType(type_)
        self.status = ComponentInstanceState(status)
        if created_by:
            self.created_by = created_by
        self.created = created
        self.environment = environment
        self.project = project
        self._component_id = component_id
        self._kubernetes_name = kubernetes_name

    def __repr__(self):
        return f"id [{self.id}], name [{self.name}]"

    def delete(self):
        advanced.project.delete_component_instance(self.project.id, self.environment.id, self.id)

    def wait_for_status(self, component_instance_state: ComponentInstanceState, timeout_seconds=None, poll_frequency=0.25):
        component_instance_state = str2enum(component_instance_state, ComponentInstanceState).value
        print_info(f"Waiting for status [{component_instance_state}] on "
                   f"{self.type.value} instance [{self.name}], "
                   f"environment [{self.environment.name}], "
                   f"project [{self.project.name}]")
        advanced.project.wait_for_component_instance_status(self.project.id, self.environment.id, self.id, component_instance_state, timeout_seconds, poll_frequency)

    def get_url(self):
        if self.type == ComponentType.APP:
            return f"{kortical_config.get('system_url')}/api/v1/projects/{self.project.name.replace(' ', '-')}/environments/{self.environment.name.replace(' ', '-')}/apps/{self.name.replace(' ', '-')}/"
        elif self.type == ComponentType.MODEL:
            return f"{kortical_config.get('system_url')}/api/v1/projects/{self.project.name.replace(' ', '-')}/environments/{self.environment.name.replace(' ', '-')}/models/{self.name.replace(' ', '-')}/"
        else:
            return None

    def get_kubernetes_name(self):
        return self._kubernetes_name

    def get_kortical_config(self):
        return advanced.project.get_component_instance_kortical_config(self.project.id, self.environment.id, self.id)

    def set_kortical_config(self, kortical_config: dict):
        return advanced.project.set_component_instance_kortical_config(self.project.id, self.environment.id, self.id, kortical_config)


# Adding static method after class definition so it has awareness of derived types and can create instances of these types
from kortical.api.app_instance import AppInstance
from kortical.api.model_instance import ModelInstance


def _create_from_json(cls, project_id, environment_id, component_instance_json):
    if component_instance_json is None:
        return None
    if component_instance_json['type'] == 'app':
        return AppInstance._create_from_json(project_id, environment_id, component_instance_json)
    elif component_instance_json['type'] == 'model':
        return ModelInstance._create_from_json(project_id, environment_id, component_instance_json)
    raise Exception(f'Cannot create ComponentInstance of type [{component_instance_json["ype"]}]')


ComponentInstance._create_from_json = classmethod(_create_from_json)
