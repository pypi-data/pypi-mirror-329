from celery.result import AsyncResult
from flask import request, Response
import logging
import pandas as pd
import time

from kortical.api.model import Model

from module_placeholder.authentication import safe_api_call
from module_placeholder.bigquery.bigquery import append_dataframe_to_bigquery
from module_placeholder.celery import celery
from module_placeholder.constants import MODEL_NAME
from module_placeholder.workflows.train import train_workflow
from module_placeholder.workflows.predict import predict_workflow


logger = logging.getLogger(__name__)


# run task in celery worker
@celery.task(bind=True, ignore_result=True)
def celery_train_workflow(self):
    data = {}
    train_workflow.execute(data=data,
                           progress_report_function=lambda x: self.update_state(state=x))


def register_routes(app):
    @app.route('/health', methods=['get'])
    def health():
        return {"result": "success"}

    @app.route('/online_learning', methods=['post'])
    def online_learning():
        """
            Uploads data, appending it to the bigquery database.
        """

        file = request.files['file']
        df = pd.read_csv(file)
        append_dataframe_to_bigquery(df)

        return {"result": "success"}

    @app.route('/train', methods=['post'])
    @safe_api_call
    def post_train():
        """
            Triggers the train workflow.
        """

        model = Model.create_or_select(MODEL_NAME)
        if model.train_status()['is_training'] is True:
            return {'error': 'Model is already training.'}

        task = celery_train_workflow.apply_async()
        max_wait_time = 60
        start_time = time.time()
        while time.time() - start_time < max_wait_time:
            if task.state != 'PENDING':
                break
            time.sleep(1)

        return {'train_id': task.task_id}

    @app.route('/train/<train_id>', methods=['get'])
    @safe_api_call
    def get_train_status(train_id):
        """
            Returns the status of a train workflow run.
        """

        result = celery.AsyncResult(train_id)
        return {'status': result.state}

    @app.route('/train/<train_id>', methods=['delete'])
    @safe_api_call
    def delete_train(train_id):
        """
            Cancels the train workflow.
        """
        model = Model.select(MODEL_NAME)
        model.train_stop()
        task = AsyncResult(train_id)
        task.revoke(terminate=True)
        return {"result": "success"}

    @app.route('/predict', methods=['post'])
    @safe_api_call
    def predict():
        """
            Triggers the predict workflow.
        """

        file = request.files['file']
        df = pd.read_csv(file)

        result_data = predict_workflow.execute(data={'df': df}, progress_report_function=lambda x: print(x))
        df_out = result_data['df_out']

        response = Response(df_out.to_csv(index=False), content_type="text/csv")
        response.headers["Content-Disposition"] = "attachment; filename=data.csv"
        return response
