import os
from datetime import datetime
from kortical.api import advanced
from kortical.api.environment import Environment
from kortical.cloud.cloud import IS_KUBERNETES_ENVIRONMENT
from kortical.config import kortical_config

from kortical.helpers.exceptions import KorticalKnownException


class Project:

    @classmethod
    def _create_from_json(cls, project_json):
        created = datetime.strptime(project_json['created']['__value__'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        project = cls(id_=project_json['id'],
                      name=project_json['name'],
                      created=created,
                      created_by=project_json.get('created_by'))
        return project

    @classmethod
    def create_project(cls, project_name, comma_separated_environment_names=None):
        return cls._create_from_json(advanced.project.create_project(project_name, comma_separated_environment_names))

    @classmethod
    def list(cls, include_created_by=False):
        projects_list_json = advanced.project.list_projects(include_created_by=include_created_by)
        return [cls._create_from_json(x) for x in projects_list_json]

    @classmethod
    def get_project(cls, project_name_or_id):
        project_json = advanced.project.get_project(project_name_or_id)
        project = cls._create_from_json(project_json) if project_json else None
        return project

    @classmethod
    def get_selected_project(cls, throw=True):
        if IS_KUBERNETES_ENVIRONMENT:
            selected_project_id = os.environ['KORE_PROJECT_ID']
        else:
            selected_project_id = kortical_config.get('selected_project_id')
        project_json = advanced.project.get_project(selected_project_id)
        project = cls._create_from_json(project_json) if project_json else None
        if project is None and throw:
            raise KorticalKnownException(f"No project selected.")
        return project

    @classmethod
    def deselect_project(cls):
        kortical_config.set('selected_project_id', None, print=False)
        kortical_config.set('selected_environment_id', None, print=False)

    def __init__(self, id_, name, created, created_by=None):
        self.id = id_
        self.name = name
        if created_by:
            self.created_by = created_by
        self.created = created

    def __repr__(self):
        return f"id [{self.id}], name [{self.name}]"

    def select(self, print=False):
        kortical_config.set('selected_project_id', self.id, print=print)

    def delete(self):
        return advanced.project.delete_project(self.id)

    def list_environments(self):
        environments = Environment.list(self)
        return environments

    def get_environment(self, environment_name_or_id):
        return Environment.get_environment(self, environment_name_or_id)

    def get_kortical_config(self):
        return advanced.project.get_project_kortical_config(self.id)

    def set_kortical_config(self, kortical_config : dict):
        return advanced.project.set_project_kortical_config(self.id, kortical_config)
