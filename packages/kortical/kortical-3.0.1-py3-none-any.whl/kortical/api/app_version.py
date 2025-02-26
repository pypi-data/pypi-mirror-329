from datetime import datetime
from kortical.api import advanced


class AppVersion:

    @classmethod
    def _create_from_json(cls, app_version_json):
        created = datetime.strptime(app_version_json['created']['__value__'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        return cls(
            id_=app_version_json["id"],
            name=app_version_json["name"],
            version=app_version_json["version"],
            created=created,
            description=app_version_json['description'] if app_version_json.get('description') else 'None',
            app_config=app_version_json.get("app_config"),
            created_by=app_version_json.get("created_by"),
            _type=app_version_json['type'],
            _component_id=app_version_json["component_id"]
        )

    @classmethod
    def list(cls, app, include_created_by=False):
        app_versions_json = advanced.app.list_app_versions(app.id, include_created_by)
        return [cls._create_from_json(x) for x in app_versions_json]

    @classmethod
    def get_version(cls, app, version_name_or_id):
        app_version_json = advanced.app.get_app_version(app.id, version_name_or_id)
        app_version = cls._create_from_json(app_version_json) if app_version_json else None
        return app_version
    
    @classmethod
    def create_version(cls, app, k8s_config, app_config=None):
        app_version_json = advanced.app.create_app_version(app.id, k8s_config, app_config)
        app_version = AppVersion._create_from_json(app_version_json)
        return app_version

    def __init__(self, id_, name, version, created, _type, _component_id, description=None, app_config=None, created_by=None):
        self.id = id_
        self.name = name
        self.version = f'v{version}' if version is not None else None
        if description:
            self.description = description
        if app_config:
            self.app_config = app_config
        if created_by:
            self.created_by = created_by
        self.created = created
        self._type = _type
        self._component_id = _component_id

    def __repr__(self):
        return f"id [{self.id}] v[{self.version[1:] if self.version is not None else None}]"

    def get_app_version_config(self):
        return advanced.app.get_app_version_config(self.name, self.id)

    def set_app_version_config(self, app_config):
        return advanced.app.set_app_version_config(self.name, self.id, app_config)

    def set_description(self, description):
        return advanced.app.set_app_version_description(self.name, self.id, description)
