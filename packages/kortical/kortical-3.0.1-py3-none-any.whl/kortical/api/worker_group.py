from kortical.api import advanced


class WorkerGroup:

    @classmethod
    def _create_from_json(cls, worker_group_json):
        return cls(
            id_=worker_group_json["id"],
            name=worker_group_json["name"],
            state=worker_group_json['state'],
            worker_type=worker_group_json['worker_type'],
            current_size=worker_group_json['current_size'],
            required_size=worker_group_json['required_size']
        )

    @classmethod
    def create_worker_group(cls, worker_group_name, worker_type, size):
        return cls._create_from_json(advanced.worker_group.create_worker_group(worker_group_name, worker_type, size))

    @classmethod
    def list(cls):
        return [cls._create_from_json(x) for x in advanced.worker_group.list_worker_groups()]

    @classmethod
    def get_worker_group(cls, worker_group_or_id):
        worker_group_json = advanced.worker_group.get_worker_group(worker_group_or_id)
        worker_group = cls._create_from_json(worker_group_json) if worker_group_json else None
        return worker_group

    @classmethod
    def list_worker_types(cls):
        return advanced.worker_group.list_worker_types()

    @classmethod
    def default_worker_type(cls):
        return advanced.worker_group.get_default_worker_type()

    def __init__(self, id_, name, state, worker_type, current_size, required_size):
        self.id = id_
        self.name = name
        self.state = state
        self.worker_type = worker_type
        self.current_size = current_size
        self.required_size = required_size

    def delete(self):
        return advanced.worker_group.delete_worker_group(self.id)

    def resize(self, size):
        return self._create_from_json(advanced.worker_group.update_worker_group(self.id, required_size=size))

