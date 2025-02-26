from enum import Enum


class ExplainProfile(Enum):
    FAST = 'fast'
    ACCURATE = 'accurate'
    EXHAUSTIVE = 'exhaustive'


class ComponentType(Enum):
    APP = 'app'
    MODEL = 'model'


class ComponentInstanceState(Enum):
    CREATING = 'Creating'
    PENDING = 'Pending'
    RUNNING = 'Running'
    FAILED = 'Failed'
    TERMINATING = 'Terminating'
    TERMINATED = 'Terminated'
