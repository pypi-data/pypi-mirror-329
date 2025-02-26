from datetime import datetime

from kortical.api import advanced


class ModelVersion:

    @classmethod
    def _create_from_json(cls, model_version_json):
        created = datetime.strptime(model_version_json['created']['__value__'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        return cls(
            id_=model_version_json["id"],
            name=model_version_json["name"],
            version=model_version_json["version"],
            description=model_version_json.get('description') if model_version_json.get('description') else 'None',
            created=created,
            created_by=model_version_json.get('created_by'),
            model_type=model_version_json['model_type'],
            score=model_version_json['score'],
            score_type=model_version_json['score_type'],
            _is_max=model_version_json['_is_max'],
            _type=model_version_json['type'],
            _component_id=model_version_json["component_id"]
        )

    @classmethod
    def list(cls, model, include_created_by=False):
        model_version_list_json = advanced.model.list_model_versions(model.id, include_created_by)
        return [cls._create_from_json(x) for x in model_version_list_json]

    @classmethod
    def get_version(cls, model, version_name_or_id):
        model_version_json = advanced.model.get_model_version(model.id, version_name_or_id)
        model_version = cls._create_from_json(model_version_json) if model_version_json else None
        return model_version

    def __init__(self, id_, name, version, created, model_type, score, score_type, _is_max, _type, _component_id, description=None, created_by=None):
        self.id = id_
        self.name = name
        self.version = f'v{version}' if version is not None else None
        self.model_type = model_type
        self.score = score
        self.score_type = score_type
        if description:
            self.description = description
        if created_by:
            self.created_by = created_by
        self.created = created
        self._is_max = _is_max
        self._type = _type
        self._component_id = _component_id

    def __repr__(self):
        return f"id [{self.id}] v[{self.version[1:] if self.version is not None else None}]"

    def set_description(self, description):
        return advanced.model.set_model_version_description(self.name, self.id, description)
