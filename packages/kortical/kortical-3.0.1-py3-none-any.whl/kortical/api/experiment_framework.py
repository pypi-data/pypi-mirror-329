import os
import colorama
import datetime
import numbers
import shutil
import yaml
import pandas as pd

from kortical.api.model_version import ModelVersion

from kortical.helpers.type_conversion import clean_numpy_types_from_dict
from kortical.helpers.print_helpers import print_error, print_success, print_warning


# Store/access results of various training runs using the folder structure '{path}.experiments/experiment/results'
class ExperimentFramework:

    @staticmethod
    def _write_results(results, path):
        # Store model details at results level in individual files
        result_path = os.path.join(path, "results")
        os.mkdir(result_path)
        for count, result in enumerate(results):
            _model = result[0]
            model_path = os.path.join(result_path, f"model_{count + 1}.yaml")

            model_dict = {"id": _model.id,
                          "name": _model.name,
                          "version": _model.version,
                          "created": _model.created,
                          "model_type": _model.model_type,
                          "score_type": _model.score_type,
                          "score": _model.score,
                          "_is_max": _model._is_max,
                          "custom_loss": result[1] if not hasattr(result[1], 'item') else result[1].item(),
                          # convert from numpy to regular type
                          "format_result": result[2]}

            with open(model_path, "w") as f:
                yaml.dump(model_dict, f)

    def __init__(self, path=".experiments", is_minimising=True):
        self.framework_path = path
        self.is_minimising = is_minimising

        # Create framework using path, if it does not exist
        if not os.path.exists(self.framework_path):
            os.mkdir(self.framework_path)
            print_success(f"[{self.framework_path}] folder created successfully.")
        else:
            print_error(f"[{self.framework_path}] folder already exists.")

    def __enter__(self):
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        if exception_type is None:
            self.print_experiment_results()

    def list_experiments(self):
        # need to call next() because os.walk is a generator obj and we need to get at its return tuple
        # os.walk returns a tuple (dirpath, dirnames, filenames). - we are interested in the dirnames only hence [1]
        return next(os.walk(self.framework_path))[1]

    def _create_experiment(self, name):
        experiments = self.list_experiments()

        # Count occurrences of experiment names (ignoring run number)
        run_number = len([x for x in experiments if x == name])
        run_number += len([x for x in experiments if x.startswith(f"{name}_")])

        if run_number == 0:
            exp_name = f'{name}'
        else:
            exp_name = f'{name}_{run_number}'

        exp_path = os.path.join(self.framework_path, exp_name)
        os.mkdir(exp_path)

        print_success(f"[{exp_name}] folder created successfully.")

        return exp_name, exp_path

    def clear_experiment_cache(self):
        # Wipe all experiments and results in framework
        for root, dirs, files in os.walk(self.framework_path):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

        print_warning("All experiments and results deleted.")

    def record_experiment(self, experiment_name, results=None, model_version=None, description=None, custom_artifact_paths=None, tags=None):

        # Validate results and model (2 acceptable formats)
        # Case 1: results = [(model, num, str),...] and model=None / Case 2: A single model and result
        # Convert case 2 to case 1 so all results have same format
        if results is None:
            results = ((model_version, model_version.score, f"{model_version.score} {model_version.score_type}"),)
        elif isinstance(results, numbers.Number):
            if model_version is None:
                raise Exception("If passing in results as a number then model_version cannot be null")
            else:
                results = ((model_version, results, f"Result: {results}, Best Model Score: {model_version.score} {model_version.score_type}"),)
        elif isinstance(results, (list, tuple)):
            if len(results) == 0:
                raise Exception("Results cannot be a zero length list.")
            for result in results:
                if isinstance(result, (tuple, list)) \
                        and isinstance(result[0], ModelVersion) \
                        and isinstance(result[1], numbers.Number) \
                        and isinstance(result[2], str):
                    pass
                else:
                    raise Exception(
                        f"Results [{result}] is not a valid format. It should either be the model / custom loss "
                        f"function score or the results list returned by train_model_custom_loss_on_top_n"
                        )
        else:
            raise Exception(
                f"Results [{results}] invalid. It should either be the model / custom loss function score or "
                f"the results list returned by train_model_custom_loss_on_top_n"
                )
        result = results[0]

        # Validate custom artifact paths: either str or [str,...]
        if custom_artifact_paths is not None:
            if type(custom_artifact_paths) is str:
                custom_artifact_paths = [custom_artifact_paths]
            for path in custom_artifact_paths:
                if type(path) is str and os.path.exists(path):
                    pass
                else:
                    raise Exception(f"Invalid artifact path [{path}].")

        # Create experiment folder, prepare data for storage
        experiment_name, experiment_path = self._create_experiment(experiment_name)

        if tags is not None:
            tags = clean_numpy_types_from_dict(tags)

        experiment_overview_path = os.path.join(experiment_path, f"overview.yaml")
        overview_dict = {"experiment_name": experiment_name,
                         "description": description,
                         "custom_artifact_path": custom_artifact_paths,
                         "datetime": datetime.datetime.now().strftime("%Y/%m/%d, %H:%M:%S"),
                         "tags": tags}
        experiment_best_model_path = os.path.join(experiment_path, f"best_model.yaml")
        best_model = result[0]
        best_model_dict = {"id": best_model.id,
                           "name": best_model.name,
                           "version": best_model.version,
                           "created": best_model.created,
                           "model_type": best_model.model_type,
                           "score_type": best_model.score_type,
                           "score": best_model.score,
                           "_is_max": best_model._is_max,
                           "_component_id": best_model._component_id,
                           "custom_loss": result[1] if not hasattr(result[1], 'item') else result[1].item(),  # convert from numpy to regular type
                           "format_result": result[2]}

        # Store overview, best_model, full results and custom artifacts
        with open(experiment_overview_path, "w") as f:
            yaml.dump(overview_dict, f)
        with open(experiment_best_model_path, "w") as f:
            yaml.dump(best_model_dict, f)
        self._write_results(results, experiment_path)
        if custom_artifact_paths:
            for path in custom_artifact_paths:
                shutil.copy(path, experiment_path)

        self._save_results_table(self.get_experiment_results())
        self.print_experiment_results(highlight_experiment=experiment_name)

    def get_experiment_results(self, order_by='custom_loss'):

        # Validate user input if present
        order_by_args = ['custom_loss', 'score', 'time']
        if order_by not in order_by_args:
            raise Exception(f'Invalid argument for ordering. Select one of {order_by_args}')

        experiments = self.list_experiments()
        if experiments == []:
            raise Exception("No experiments.")

        experiment_results = []

        # Extract information from yaml files
        for experiment_name in experiments:
            model_path = os.path.join(self.framework_path, experiment_name, "best_model.yaml")
            with open(model_path) as f:
                best_model = yaml.safe_load(f)
            overview_path = os.path.join(self.framework_path, experiment_name, f"overview.yaml")
            with open(overview_path) as f:
                overview = yaml.safe_load(f)

            # Set metric
            if order_by == 'score' or order_by == 'time':
                metric = 'score'
            else:
                metric = 'custom_loss'
                if metric not in best_model:
                    raise Exception(f"Attribute {metric} not found in model")

            experiment_results.append({'experiment_name': experiment_name, 'best_model_score': best_model[metric], 'score_metric_used': metric, 'model_info': best_model, 'experiment_info': overview})

        if order_by == 'time':
            experiment_results.sort(key=lambda x: x['experiment_info']['datetime'])
        else:
            experiment_results.sort(reverse=not self.is_minimising, key=lambda x: x['best_model_score'])

        return experiment_results

    def get_best_model_version(self, experiment_name=None):

        if experiment_name == None:
            results_path = os.path.join(self.framework_path, "results_table.csv")
            results_df = pd.read_csv(results_path)
            experiment_name = results_df['experiment_name'][0]
        elif experiment_name not in self.list_experiments():
            raise Exception(f'Experiment [{experiment_name}] not found.')

        best_model_path = os.path.join(self.framework_path, experiment_name, 'best_model.yaml')
        with open(best_model_path) as f:
            best_model = yaml.safe_load(f)

        return ModelVersion(id_=best_model['id'],
                            name=best_model['name'],
                            _type='model',
                            version=best_model['version'],
                            created=best_model['created'],
                            model_type=best_model['model_type'],
                            score=best_model['score'],
                            score_type=best_model['score_type'],
                            _is_max=best_model['_is_max'],
                            _component_id=best_model['_component_id'],
                            created_by=None)

    def _print_experiment(self, index, experiment, highlight=True):
        brightness = colorama.Style.BRIGHT if highlight else colorama.Style.DIM
        if brightness == colorama.Style.BRIGHT:
            if experiment['experiment_info']['tags'] is not None:
                print(colorama.Fore.LIGHTYELLOW_EX + f"{index}. " +
                      colorama.Fore.LIGHTCYAN_EX + colorama.Style.BRIGHT +
                      f"{experiment['experiment_name']}. {experiment['model_info']['format_result']} at {experiment['experiment_info']['datetime']}\n"
                      f"custom tags: {', '.join([f'{k}={v}' for k, v in experiment['experiment_info']['tags'].items()])}" + colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.LIGHTYELLOW_EX + f"{index}. " + colorama.Fore.LIGHTCYAN_EX + colorama.Style.BRIGHT + f"{experiment['experiment_name']}. "
                                                                                                                             f"{experiment['model_info']['format_result']} at "
                                                                                                                             f"{experiment['experiment_info']['datetime']} " + colorama.Style.RESET_ALL)
        else:
            if experiment['experiment_info']['tags'] is not None:
                print(colorama.Fore.YELLOW + f"{index}. " + colorama.Fore.CYAN +  colorama.Style.BRIGHT + f"{experiment['experiment_name']}. "
                                                                                                              f"{experiment['model_info']['format_result']} at "
                                                                                                              f"{experiment['experiment_info']['datetime']}\ncustom tags: {', '.join([f'{k}={v}' for k, v in experiment['experiment_info']['tags'].items()])}" + colorama.Style.RESET_ALL)
            else:
                print(colorama.Fore.YELLOW + f"{index}. " + colorama.Fore.CYAN + colorama.Style.BRIGHT + f"{experiment['experiment_name']}. "
                                                                                                             f"{experiment['model_info']['format_result']} at "
                                                                                                             f"{experiment['experiment_info']['datetime']}" + colorama.Style.RESET_ALL)
        brightness = colorama.Style.NORMAL if highlight else colorama.Style.DIM
        if experiment['experiment_info']['description'] is not None:
            print(brightness + colorama.Fore.GREEN + f"description: {experiment['experiment_info']['description']}" + colorama.Style.RESET_ALL)
        print(brightness + colorama.Fore.GREEN + f"version_id: {experiment['model_info']['id']}, "
                                                 f"model_type: {experiment['model_info']['model_type']}, "
                                                 f"score: {experiment['model_info']['score']}, "
                                                 f"score_type: {experiment['model_info']['score_type']}, " + colorama.Style.RESET_ALL)

    def print_experiment_results(self, order_by='custom_loss', highlight_experiment=None):

        experiment_results = self.get_experiment_results(order_by)

        # Print chronological experiment list
        if order_by == 'time':
            print(colorama.Fore.LIGHTYELLOW_EX + f"\nChronological experiment list:\n")
            for i in range(len(experiment_results)):
                experiment = experiment_results[i]
                self._print_experiment(experiment['experiment_info']['datetime'], experiment)
            return

        # Printed highlighted experiment at beginning, then ranked list
        if highlight_experiment is not None:
            print(colorama.Fore.LIGHTYELLOW_EX + f"\n\nCurrent experiment:\n")

            found = False
            for i in range(len(experiment_results)):
                experiment = experiment_results[i]
                if experiment['experiment_name'] == highlight_experiment:
                    self._print_experiment(i+1, experiment, True)
                    found = True
                    break
            if not found:
                raise Exception(f"No experiment [{experiment['experiment_name']}] to highlight.")

        print(colorama.Fore.LIGHTYELLOW_EX + f"\nExperiment list, ranked by {order_by}:\n")
        for i in range(len(experiment_results)):
            experiment = experiment_results[i]
            self._print_experiment(i+1, experiment, True if highlight_experiment is None else highlight_experiment == experiment['experiment_name'])

    def _save_results_table(self, results_list):
        experiment_results_table_path = os.path.join(self.framework_path,'results_table.csv')
        results_table = pd.DataFrame(results_list)
        tag_columns_series = results_table['experiment_info'].apply(lambda x: x['tags'])
        if tag_columns_series is not None:
            tag_df = pd.DataFrame(tag_columns_series.tolist())
            results_table_with_tags = pd.concat([results_table, tag_df], axis=1)
            results_table_with_tags.to_csv(experiment_results_table_path, index=False)
        else:
            results_table.to_csv(experiment_results_table_path, index=False)
