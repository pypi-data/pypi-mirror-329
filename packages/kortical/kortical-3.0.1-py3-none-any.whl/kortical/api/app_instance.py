from datetime import datetime

from kortical.api import advanced
from kortical.api.enums import ComponentType
from kortical.api.component_instance import ComponentInstance
from kortical.helpers import format_config


class AppInstance(ComponentInstance):

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
        return ComponentInstance.list(project, environment, ComponentType.APP, include_created_by=include_created_by, include_deleted=include_deleted)

    @classmethod
    def create_app_instance(cls, project, environment, app_name_or_version_id, wait_for_ready=False):
        app_instance = ComponentInstance.create_component_instance(project, environment, app_name_or_version_id, wait_for_ready)
        return app_instance

    @classmethod
    def get_app_instance(cls, project, environment, app_name_or_instance_id):
        app_instance = ComponentInstance.get_component_instance(project, environment, app_name_or_instance_id, component_type=ComponentType.APP)
        return app_instance

    def restart(self):
        return advanced.app.restart_app_instance(self.project.id, self.environment.id, self.id)

    def get_app_version(self):
        from kortical.api.app import App
        from kortical.api.app_version import AppVersion

        app = App.get_app(self._component_id)
        return self.version

    def get_app(self):
        from kortical.api.app import App

        app = App.get_app(self._component_id)
        return app

    def get_logs(self, replica=0):
        return advanced.project.get_component_logs(self.project.id, self.environment.id, self.id, replica)

    def get_app_config(self, format=None):
        config = advanced.app.get_app_config(self.project.id, self.environment.id, self.id)
        return format_config(config, format)

    def set_app_config(self, app_config, restart=True):
        return advanced.app.set_app_config(self.project.id, self.environment.id, self.id, app_config, restart)
