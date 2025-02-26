import inspect
from dataclasses import dataclass
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


@dataclass
class StopWatchData:
    average_time: float = 0
    iteration_count: int = 0


class StopWatch(object):

    tracker = {}

    def __init__(self, name=None):
        if name is None:
            name = inspect.stack()[1][3]

        self.name = name
        self.start = datetime.now()

        if self.name not in StopWatch.tracker:
            StopWatch.tracker[self.name] = StopWatchData()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()

    def stop(self):
        delta = (datetime.now() - self.start).total_seconds()
        data = StopWatch.tracker[self.name]
        data.average_time = (delta + data.average_time * data.iteration_count) / (data.iteration_count + 1)
        data.iteration_count += 1
        logger.info("StopWatch [{}] took [{}] seconds. Average [{}] seconds".format(self.name, delta, data.average_time))
        return delta