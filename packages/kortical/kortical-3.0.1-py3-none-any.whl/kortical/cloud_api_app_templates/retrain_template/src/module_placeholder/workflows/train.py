from module_placeholder.workflows.workflow import Workflow
from module_placeholder.workflows.steps.fetch_data_from_bigquery import FetchDataFromBigquery
from module_placeholder.workflows.steps.train_model import TrainModel
from module_placeholder.workflows.steps.compare_and_update_model import CompareAndUpdateModel

train_workflow = Workflow(steps=[
    FetchDataFromBigquery(),
    TrainModel(),
    CompareAndUpdateModel()
])
