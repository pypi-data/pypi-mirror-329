from inspect import getmembers, isfunction, ismodule
import os
from .nodes import data_node
from .nodes import data_source_file
from .nodes import data_source_csv
from .nodes import data_source_excel
from .nodes import transform as transform_function
from .nodes import report
from .nodes import save_csv
from kortical.data_flow.custom_nodes import model
from kortical.data_flow.custom_nodes import predict
from kortical.data_flow.custom_nodes import thresholds
from kortical.data_flow.custom_nodes import thresholds_apply


class DataFlowNodeApi(data_node.DataNode):

    def _handle_inputs(self, node, inputs):
        if not isinstance(inputs, (list, tuple)):
            inputs = [inputs]
        if len(inputs) > 0:
            node.add_parents(inputs)
        else:
            self.add_child(node)

    def create_data_source_node(self, cls, file_paths, name=None, inputs=[], **kwargs):
        if isinstance(file_paths, str):
            file_paths = (file_paths,)

        if name is None:
            name = os.path.splitext(os.path.basename(file_paths[0]))[0]
        if 'data_source_name' not in kwargs:
            node = cls(file_paths, data_source_name=name, **kwargs)
        else:
            node = cls(file_paths, **kwargs)
        self._handle_inputs(node, inputs)
        return node

    def create_data_source_file_node(self, file_paths, name=None, inputs=[], **kwargs):
        return self.create_data_source_node(data_source_file.DataSourceFile, file_paths, name, inputs, **kwargs)

    def create_data_source_csv_node(self, file_paths, name=None, inputs=[], **kwargs):
        return self.create_data_source_node(data_source_csv.DataSourceCsv, file_paths, name, inputs, **kwargs)

    def create_data_source_excel_node(self, file_paths, name=None, inputs=[], **kwargs):
        return self.create_data_source_node(data_source_excel.DataSourceExcel, file_paths, name, inputs, **kwargs)

    def create_transform_node(self, function, name=None, inputs=[]):
        if name is None:
            name = transform_function.Transform.get_transform_name(function)
        node = transform_function.Transform(name, function)
        self._handle_inputs(node, inputs)
        return node

    def create_report_node(self, function, name=None, inputs=[]):
        if name is None:
            name = transform_function.Transform.get_transform_name(function)
        node = report.Report(name, function)
        self._handle_inputs(node, inputs)
        return node

    def create_save_csv_node(self, file_path, data_source_name, name=None, inputs=[]):
        if name is None:
            name = os.path.splitext(os.path.basename(file_path))[0]
        node = save_csv.SaveCsv(name, file_path, data_source_name)
        self._handle_inputs(node, inputs)
        return node

    def create_model_node(self, kortical_url, data_source_train, model_code=None, targets=None, number_of_train_workers=None, minutes_to_train=60, max_models_with_no_score_change=200, name=None, inputs=[]):
        node = model.Model(kortical_url, data_source_train, model_code, targets, number_of_train_workers, minutes_to_train, max_models_with_no_score_change, name)
        self._handle_inputs(node, inputs)
        return node

    def create_predict_node(self, kortical_url, data_source, model_id=None, instance_name=None, deployment_name=None, name=None, inputs=[]):
        node = predict.Predict(kortical_url, data_source, model_id, instance_name, deployment_name, name)
        self._handle_inputs(node, inputs)
        return node

    def create_thresholds_node(self, kortical_url, thresholds_id, data_source_fit, data_source_test, targets, target_accuracy, non_automated_class=None, name=None, inputs=[]):
        node = thresholds.Thresholds(kortical_url, thresholds_id, data_source_fit, data_source_test, targets, target_accuracy, non_automated_class, name)
        self._handle_inputs(node, inputs)
        return node

    def create_apply_thresholds_node(self, kortical_url, thresholds_id, data_source, targets, non_automated_class=None, name=None, inputs=[]):
        node = thresholds_apply.ApplyThresholds(kortical_url, thresholds_id, data_source, targets, non_automated_class, name)
        self._handle_inputs(node, inputs)
        return node


# Add hooks
def add_tests(self, tests):
    if not isinstance(tests, (list, tuple)):
        tests = [tests]
    t = []
    for test in tests:
        if ismodule(test):
            _tests = getmembers(test, lambda x: isfunction(x) and x.__name__.startswith('ktest_'))
            for _test in _tests:
                node = transform_function.Transform(_test[0], _test[1])
                t.append(node)
        elif isfunction(test):
            name = transform_function.Transform.get_transform_name(test)
            node = transform_function.Transform(name, test)
            t.append(node)
        else:
            t.append(test)
    self._tests = t
    return self

# We use a hook because Transform is an implementation of DataNode, so we couldn't make it a regular member function due to circular dependencies
data_node.DataNode.add_tests = add_tests