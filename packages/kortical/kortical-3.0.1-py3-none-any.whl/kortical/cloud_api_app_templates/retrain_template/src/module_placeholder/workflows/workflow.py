import datetime
import logging

logger = logging.getLogger(__name__)


"""This class executes a simple workflow

Because of python's duck typing we don't have well defined
interfaces. Substitutable steps are expected to be
able to consume the same input object and return an
equivalent output object for use by the next step."""


class Workflow:

    def __init__(self, steps):
        self.steps = steps
        self.timings = []

    def execute(self, data=None, progress_report_function=None):
        logger.info("Executing first step [%s].", self.steps[0].__class__)
        output = self.steps[0].execute(data, progress_report_function)
        input = output
        for step in self.steps[1:]:
            logger.info("Executing step [%s].", step.__class__)
            t0 = datetime.datetime.utcnow()
            output = step.execute(input, progress_report_function)
            runtime = datetime.datetime.utcnow() - t0
            self.timings.append([step.__class__,'{} days {}'.format(runtime.days,str(runtime))])
            logger.info(f"Step [{step.__class__}] took {self.timings[-1][1]}")
            input = output
        logger.info("Finished executing workflow.")
        return output
