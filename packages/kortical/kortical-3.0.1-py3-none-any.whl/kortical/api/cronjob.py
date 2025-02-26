from datetime import datetime

from kortical.api import advanced


class Cronjob:

    @classmethod
    def _create_from_json(cls, project, environment, cronjob_json):
        created = datetime.strptime(cronjob_json['created']['__value__'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        return cls(
            id_=cronjob_json['id'],
            name=cronjob_json['name'],
            status=cronjob_json['status'],
            cron_time_string=cronjob_json['cron_time_string'],
            url=cronjob_json['url'],
            url_headers=cronjob_json['url_headers'],
            created=created,
            environment=environment,
            project=project
        )

    @classmethod
    def create_cronjob(cls, project, environment, cronjob_name, time_parameters, url, url_headers=None):
        url_headers = url_headers if url_headers is not None else {}
        cronjob_json = advanced.cronjob.create_cronjob(project.id, environment.id, cronjob_name, time_parameters, url, url_headers)
        cronjob = cls._create_from_json(project, environment, cronjob_json)
        return cronjob

    @classmethod
    def list(cls, project, environment):
        cronjobs_json = advanced.cronjob.list_cronjobs(project.id, environment.id)
        cronjobs = [cls._create_from_json(project, environment, x) for x in cronjobs_json]
        return cronjobs

    @classmethod
    def get_cronjob(cls, project, environment, cronjob_name_or_id):
        cronjob_json = advanced.cronjob.get_cronjob(project.id, environment.id, cronjob_name_or_id)
        cronjob = cls._create_from_json(project, environment, cronjob_json) if cronjob_json else None
        return cronjob

    def __init__(self, project, environment, id_, name, status, cron_time_string, url, url_headers, created):
        self.id = id_
        self.name = name
        self.status = status
        self.cron_time_string = cron_time_string
        self.url = url
        self.url_headers = url_headers
        self.created = created
        self.environment = environment
        self.project = project

    def __repr__(self):
        return f"id [{self.id}], name [{self.name}]"

    def update(self, time_parameters=None, url=None, url_headers=None):
        cronjob_json = advanced.cronjob.update_cronjob(self.project.id, self.environment.id, self.id, time_parameters, url, url_headers)
        self.cron_time_string = cronjob_json['cron_time_string']
        self.url = cronjob_json['url']
        self.url_headers = cronjob_json['url_headers']
        return self

    def delete(self):
        advanced.cronjob.delete_cronjob(self.project.id, self.environment.id, self.id)
