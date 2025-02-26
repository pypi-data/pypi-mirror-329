from datetime import datetime

from kortical.api import advanced
from kortical.api.model_version import ModelVersion
from kortical.api.project import Project
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_info, print_error, print_success


class Model:

    @classmethod
    def _create_from_json(cls, model_json):
        created = datetime.strptime(model_json['created']['__value__'][:-1], "%Y-%m-%dT%H:%M:%S.%f")
        return cls(
            id_=model_json['id'],
            name=model_json['name'],
            created=created,
            created_by=model_json.get('created_by'),
            status=model_json['status'],
            score_type=model_json['score_type'],
            score=model_json['score'],
            train_worker_group=model_json['train_worker_group'],
            default_component_version_id=model_json['default_component_version_id']
        )

    @classmethod
    def select(cls, model_name, delete_unpublished_versions=False, stop_train=False):
        model = cls.get_model(model_name)
        if model is not None:
            if delete_unpublished_versions:
                model.delete_unpublished_versions()
            if stop_train:
                model.train_stop()
        else:
            raise KorticalKnownException(f"Unable to select model [{model_name}]")
        advanced.model.select_model(model.id)
        return model

    @classmethod
    def create_or_select(cls, model_name, delete_unpublished_versions=False, stop_train=False):
        model = cls.get_model(model_name)
        if model is not None:
            if delete_unpublished_versions:
                model.delete_unpublished_versions()
            if stop_train:
                model.train_stop()
        else:
            print_info(f"Creating model [{model_name}]")
            model_json = advanced.model.create_model(model_name)
            model = cls._create_from_json(model_json)
        print_info(f"Selecting model [{model_name}]")
        advanced.model.select_model(model.id)
        return model

    @classmethod
    def list(cls, include_created_by=False):
        return [cls._create_from_json(x) for x in advanced.model.list_models(include_created_by)]

    @classmethod
    def get_model(cls, model_name_or_id):
        model_json = advanced.model.get_model(model_name_or_id)
        model = cls._create_from_json(model_json) if model_json else None
        return model

    def __init__(self, id_, name, created, status, score_type, score, train_worker_group, default_component_version_id, created_by=None):
        self.id = id_
        self.name = name
        self.status = status
        self.score = score
        self.score_type = score_type
        self.default_version = ModelVersion.get_version(self, default_component_version_id)
        self.train_worker_group = train_worker_group
        if created_by:
            self.created_by = created_by
        self.created = created
        self._project = Project.get_project(f"model-{self.name}")

    def __repr__(self):
        return f"id [{self.id}], name [{self.name}]"

    def train_model(
            self,
            train_data,
            model_code=None,
            number_of_train_workers=None,
            max_models_with_no_score_change=None,
            max_minutes_to_train=None,
            target_score=None):

        # Train models
        if model_code is None:
            model_code = train_data.get_code()
        self.train_start(train_data, model_code)
        if number_of_train_workers:
            advanced.model.set_num_train_workers(self.id, number_of_train_workers)
        train_status = advanced.model.wait_for_training(self.id, max_models_with_no_score_change, max_minutes_to_train, target_score)

        best_model_version = self.get_version(train_status['top_models'][0]["id"])
        return best_model_version

    def train_model_custom_loss_on_top_n(
            self,
            train_data,
            test_data,
            custom_loss_function,
            custom_loss_function_kwargs=None,
            model_code=None,
            number_of_train_workers=None,
            max_models_with_no_score_change=50,
            max_minutes_to_train=None,
            n=10,
            is_minimising=True):

        # Train models like previous
        if model_code is None:
            model_code = train_data.get_code()
        self.train_start(train_data, model_code)
        if number_of_train_workers:
            advanced.model.set_num_train_workers(self.id, number_of_train_workers)
        train_status = advanced.model.wait_for_training(self.id, max_models_with_no_score_change, max_minutes_to_train)

        # Initialise list of top n models
        best_model_versions = [self.get_version(m["id"]) for m in train_status['top_models'][:n]]

        results = []
        if custom_loss_function_kwargs is None:
            custom_loss_function_kwargs = {}

        integration = self.get_environment()

        for candidate in best_model_versions:
            # Deploy to integration, predict, calculate custom loss, append to results
            model_instance = integration.create_component_instance(candidate.id, wait_for_ready=True)
            model_predictions = model_instance.predict(df=test_data)
            model_custom_loss, format_result = custom_loss_function(model_predictions, **custom_loss_function_kwargs)
            result = (candidate, model_custom_loss, format_result)
            results.append(result)

        # Sort by custom loss and return
        results = sorted(results, key=lambda x: x[1])
        if not is_minimising:
            results.reverse()
        return results

    def train_start(self, data, model_code):
        data.validate_code(model_code)
        print_info(f"Starting training for model [{self.name}], data [{data.id}|{data.name}]")
        run_id = advanced.model.train_start(self.id, data.id, model_code)
        return run_id

    def train_stop(self):
        print_info(f"Stopping training for model [{self.name}]")
        advanced.model.train_stop(self.id)

    def train_status(self):
        train_status = advanced.model.train_status(self.id)
        # potentially objectify in future
        return train_status

    def list_versions(self, include_created_by=False):
        model_versions = ModelVersion.list(self, include_created_by)
        return model_versions

    def get_version(self, version_name_or_id):
        model_version = ModelVersion.get_version(self, version_name_or_id)
        return model_version

    def set_default_version(self, model_version, wait_for_ready=True):
        model_version = ModelVersion._create_from_json(advanced.model.set_default_model_version(self.id, model_version.id))
        model_environment = self.get_environment()
        model_environment.create_component_instance(model_version.id, wait_for_ready=wait_for_ready)
        self.default_version = model_version
        return model_version

    def get_development_model_instance(self):
        model_environment = self.get_environment()
        model_instance = model_environment.get_component_instance(self.name)
        return model_instance

    def get_environment(self):
        model_environment = self._project.list_environments()[0]
        return model_environment

    def delete_version(self, model_version):
        return advanced.model.delete_model_version(self.id, model_version.id)

    def delete_unpublished_versions(self):
        print_info(f"Deleting unpublished versions for model [{self.name}]")
        return advanced.model.delete_unpublished_versions(self.id)

    def activate(self):
        return advanced.model.activate_model(self.id)

    def deactivate(self):
        return advanced.model.deactivate_model(self.id)

    def delete(self):
        return advanced.model.delete_model(self.id)
