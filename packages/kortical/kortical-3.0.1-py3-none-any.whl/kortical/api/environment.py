import os
from collections import deque
from datetime import datetime
from kortical.api import advanced
from kortical.api.cronjob import Cronjob
from kortical.api.enums import ComponentInstanceState
from kortical.api.component_instance import ComponentInstance
from kortical.cloud.cloud import IS_KUBERNETES_ENVIRONMENT
from kortical.config import kortical_config
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers import format_config


class Environment:

    @classmethod
    def _create_from_json(cls, project, environment_json):
        created = datetime.strptime(environment_json['created']['__value__'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        return cls(
            id_=environment_json['id'],
            name=environment_json['name'],
            created_by=environment_json.get('created_by'),
            created=created,
            project=project,
            promotes_to_environment_id=environment_json['promotes_to_environment_id'],
            is_challenger=environment_json['is_challenger']
        )

    @classmethod
    def create_environment(cls, project, environment_name, promotes_to_environment_name_or_id=None, component_config=None):
        return cls._create_from_json(project, advanced.project.create_environment(project.id, environment_name, promotes_to_environment_name_or_id, component_config))

    @classmethod
    def list(cls, project, include_created_by=False):
        environments_list_json = advanced.project.list_environments(project.id, include_created_by)
        environments = [cls._create_from_json(project, x) for x in environments_list_json]
        ordered_environments = deque()
        promote_id_to_find = None

        # Not efficient algorithmically but should be fine
        for _ in environments:
            for environment in environments:
                next_environment_id = environment.promotes_to_environment.id if environment.promotes_to_environment is not None else None

                if next_environment_id == promote_id_to_find or (next_environment_id is None and promote_id_to_find is None):
                    ordered_environments.appendleft(environment)
                    promote_id_to_find = environment.id

        return list(ordered_environments)

    @classmethod
    def get_environment(cls, project, environment_name_or_id):
        environment_json = advanced.project.get_environment(project.id, environment_name_or_id)
        environment = cls._create_from_json(project, environment_json) if environment_json else None
        return environment

    @classmethod
    def get_selected_environment(cls, project, throw=True):
        if IS_KUBERNETES_ENVIRONMENT:
            selected_environment_id = os.environ['KORE_ENVIRONMENT_ID']
        else:
            selected_environment_id = kortical_config.get('selected_environment_id')
        environment_json = advanced.project.get_environment(project.id, selected_environment_id)
        environment = cls._create_from_json(project, environment_json) if environment_json is not None else None
        if environment is None and throw:
            raise KorticalKnownException("No environment selected.")
        return environment

    def __init__(self, project, id_, name, created, promotes_to_environment_id, is_challenger, created_by=None):
        self.id = id_
        self.name = name
        self.promotes_to_environment = Environment.get_environment(project, promotes_to_environment_id)
        if created_by:
            self.created_by = created_by
        self.created = created
        self.project = project
        self._is_challenger = is_challenger

    def __repr__(self):
        return f"id [{self.id}], name [{self.name}]"

    def is_challenger(self):
        return self._is_challenger

    def select(self, print=False):
        kortical_config.set('selected_environment_id', self.id, print=print)

    def delete(self):
        response = advanced.project.delete_environment(self.project.id, self.id)
        if response['result'] == 'error':
            return {
                'result': 'error',
                'message': response['message'],
                'challengers': [Environment._create_from_json(self.project, challenger_json) for challenger_json in response['challengers']],
                'depending': Environment._create_from_json(self.project, response['depending']) if response['depending'] is not None else None
            }
        else:
            return response


    def list_component_instances(self, component_type=None, include_created_by=False, include_deleted=False):
        return ComponentInstance.list(self.project, self, component_type, include_created_by=include_created_by, include_deleted=include_deleted)

    def get_component_instance(self, component_name_or_instance_id, component_type=None):
        return ComponentInstance.get_component_instance(self.project, self, component_name_or_instance_id, component_type)

    def create_component_instance(self, component_name_or_version_id, wait_for_ready=False):
        return ComponentInstance.create_component_instance(self.project, self, component_name_or_version_id, wait_for_ready)

    def list_cronjobs(self):
        return Cronjob.list(self.project, self)

    def get_cronjob(self, cronjob_name_or_id):
        return Cronjob.get_cronjob(self.project, self, cronjob_name_or_id)

    def create_cronjob(self, cronjob_name, time_parameters, url, url_headers=None):
        return Cronjob.create_cronjob(self.project, self, cronjob_name, time_parameters, url, url_headers)

    def promote(self):
        advanced.project.promote_environment(self.project.id, self.id)

    def get_promotes_to_environment(self):
        if self.promotes_to_environment is None:
            return None
        return Environment.get_environment(self.project, self.promotes_to_environment.id)

    def create_challenger(self, challenger_name=None, component_config=None):
        return Environment._create_from_json(self.project, advanced.project.create_challenger_environment(self.project.id, self.id, challenger_name, component_config))

    def list_challengers(self, user_email=None):
        challenger_environments_list_json = advanced.project.list_challenger_environments(self.project.id, self.id, user_email)
        return [Environment._create_from_json(self.project, x) for x in challenger_environments_list_json]

    def get_kortical_config(self):
        return advanced.project.get_environment_kortical_config(self.project.id, self.id)

    def set_kortical_config(self, kortical_config: dict):
        return advanced.project.set_environment_kortical_config(self.project.id, self.id, kortical_config)

    def get_component_config(self):
        return advanced.project.get_component_config(self.project.id, self.id)

    def set_component_config(self, component_config : str):
        advanced.project.set_component_config(self.project.id, self.id, component_config)

    def get_environment_config(self, format=None):
        config = advanced.project.get_environment_config(self.project.id, self.id)
        return format_config(config, format)

    def set_environment_config(self, environment_config: str):
        return advanced.project.set_environment_config(self.project.id, self.id, environment_config)

    def wait_for_all_components_ready(self, timeout_seconds=None):
        timeout_seconds = timeout_seconds if timeout_seconds is not None else 180

        for component_instance in self.list_component_instances():
            component_instance.wait_for_status(ComponentInstanceState.RUNNING, timeout_seconds=timeout_seconds)
