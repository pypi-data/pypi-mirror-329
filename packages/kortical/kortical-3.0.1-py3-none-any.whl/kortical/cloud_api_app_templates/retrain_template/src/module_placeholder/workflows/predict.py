from module_placeholder.workflows.workflow import Workflow
from module_placeholder.workflows.steps.preprocess_data import PreProcessData
from module_placeholder.workflows.steps.get_prediction_from_model import GetPredictionFromModel
from module_placeholder.workflows.steps.postprocess_data import PostProcessData

predict_workflow = Workflow(steps=[
    PreProcessData(),
    GetPredictionFromModel(),
    PostProcessData()
])
