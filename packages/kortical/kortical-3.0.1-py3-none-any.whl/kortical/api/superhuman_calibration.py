import pandas as pd
import numpy as np
import enum
import colorama
from itertools import combinations, chain
from sklearn.metrics import precision_score, recall_score, f1_score
import warnings
warnings.simplefilter('module')

from kortical.helpers.print_helpers import print_info

BINARY_SEARCH_DEPTH = 12
NON_AUTOMATED_CLASS_DEFAULT = '$$Not Specified$$'


class ImportantClassesStrategy(enum.Enum):
    most_important_first = 'most_important_first'
    max_yhat_in_important_classes = 'max_yhat_in_important_classes'


def _compute_thresholds_on_label_basis(df, target, target_accuracy, important_classes,
                                       non_automated_class, important_classes_strategy, labels):
    remaining = df
    important_thresholds = {}
    num_identified_as_important_classes = 0
    num_identified_correctly_as_important_classes = 0
    original_df_length = len(remaining)
    for important_class in important_classes:
        important_thresholds[important_class] = _fit_threshold_for_label(remaining, False, important_class,
                                                                         target, target_accuracy)
        automated_accuracy_on_important_class, _, _ = _score_label_for_positive_class(remaining, False, important_class,
                                                                                      target, important_thresholds[
                                                                                          important_class])
        yhat_probs_column = f'yhat_probs_{important_class}'
        predicted_as_important_class = remaining[yhat_probs_column].gt(important_thresholds[important_class])
        if important_class == non_automated_class:
            predicted_correctly_as_important_class = pd.Series([0])
        else:
            label_is_important_class = remaining[target].eq(important_class)
            predicted_correctly_as_important_class = predicted_as_important_class & label_is_important_class

        num_identified_as_important_classes += predicted_as_important_class.sum()
        num_identified_correctly_as_important_classes += predicted_correctly_as_important_class.sum()

        print_info(f'Important class \'{important_class}\' tuned with a threshold of '
              f'{important_thresholds[important_class]} achieving an automated precision of '
              f'{automated_accuracy_on_important_class}.')

        remaining = remaining[~predicted_as_important_class]

    if len(remaining) > 0 and len(important_classes) != df[target].nunique():
        accuracy_so_far = num_identified_correctly_as_important_classes / num_identified_as_important_classes
        factor_1 = original_df_length / len(remaining)
        factor_2 = 1 - factor_1
        generic_target_accuracy = (target_accuracy * factor_1) + (factor_2 * accuracy_so_far)

        generic_threshold = _fit_threshold_for_multiple_labels(remaining, target, generic_target_accuracy,
                                                               non_automated_class)
    else:
        generic_threshold = 1

    target_dtype = df[target].dtype
    calibration_data = {
        'important_classes': important_classes,
        'important_thresholds': important_thresholds,
        'generic_threshold': generic_threshold,
        'important_classes_strategy': important_classes_strategy,
        'is_binary': False,
        'non_automated_class': non_automated_class,
        'all_classes': labels,
        'target_dtype': target_dtype,
        'target_accuracy': target_accuracy
    }
    return calibration_data


def _fit_threshold_for_label(df, is_binary, label, target, target_accuracy):
    threshold = 0.5
    label_precision, _, _ = _score_label_for_positive_class(df, is_binary, label, target, threshold)
    distance = 0.25
    for i in range(BINARY_SEARCH_DEPTH):
        up_label_precision, _, _ = _score_label_for_positive_class(df, is_binary, label, target, threshold + distance)
        down_label_precision, _, _ = _score_label_for_positive_class(df, is_binary, label, target, threshold - distance)
        if abs(target_accuracy - label_precision) >= abs(
                target_accuracy - up_label_precision) and label_precision != 1.0:
            threshold += distance
            label_precision = up_label_precision
        elif abs(target_accuracy - label_precision) >= abs(target_accuracy - down_label_precision):
            threshold -= distance
            label_precision = down_label_precision
        distance *= 0.5
    return threshold


def _fit_threshold_for_multiple_labels(df, target, target_accuracy, non_automated_class):
    threshold = 0.5
    percentage_right, _, _ = _score_prediction_multi_class(df, target, threshold, non_automated_class)
    distance = 0.25
    for i in range(BINARY_SEARCH_DEPTH):
        up_percentage_right, _, _ = _score_prediction_multi_class(df, target, threshold + distance, non_automated_class)
        down_percentage_right, _, _ = _score_prediction_multi_class(df, target, threshold - distance,
                                                                    non_automated_class)
        if abs(target_accuracy - percentage_right) >= abs(
                target_accuracy - up_percentage_right) and percentage_right != 1.0:
            threshold += distance
            percentage_right = up_percentage_right
        elif abs(target_accuracy - percentage_right) >= abs(target_accuracy - down_percentage_right):
            threshold -= distance
            percentage_right = down_percentage_right
        distance *= 0.5
    return threshold


def _score_label_for_positive_class(df, is_binary, label, target, threshold):
    # find where there were labels then percentage of positives that were right
    # find right as a proportion of all correct
    # find correct as a percentage of total dataset
    is_label = df[target] == label
    if is_binary:
        threshold_exceeded = df["yhat_probs"] > threshold
    else:
        threshold_exceeded = df[f"yhat_probs_{label}"] > threshold
    num_predicted_positive = threshold_exceeded.sum()
    predicted_label_correctly = np.logical_and(is_label, threshold_exceeded)
    num_positives_correct = predicted_label_correctly.sum()
    num_positives = is_label.sum()
    num_possible = len(df)
    label_precision = num_positives_correct / num_predicted_positive if num_predicted_positive != 0 else 0
    label_recall = num_positives_correct / num_positives
    percentage_found_of_possible = num_positives_correct / num_possible
    return label_precision, label_recall, percentage_found_of_possible


def _score_prediction_binary(df, positive_class, target, thresholds):
    is_label = df[target] == positive_class
    predicted = df[f"yhat_probs"] > thresholds['generic_threshold']
    num_predicted_positive = predicted.sum()
    correct = predicted == is_label
    correct_when_label = correct[predicted]
    num_positives_correct = correct_when_label.sum()
    accuracy = num_positives_correct / len(correct_when_label)
    automation = num_predicted_positive / len(df)
    false_positive_rate = (num_predicted_positive - num_positives_correct) / num_predicted_positive
    return accuracy, automation, false_positive_rate


def _score_prediction_multi_class(df, target, threshold, non_automated_class=None):
    yhat_probs_columns = _get_yhat_probs_columns(df)
    if non_automated_class is None:
        non_automated_class = NON_AUTOMATED_CLASS_DEFAULT
    df[target] = df[target].astype(str)
    _class = df[yhat_probs_columns].apply(_get_row_prediction, args=(non_automated_class, threshold), axis=1).astype(
        str)
    correct = df[target] == _class
    automated = _class != str(non_automated_class)
    correct_when_automated = correct[automated]
    accuracy = correct_when_automated.sum() / len(correct_when_automated)
    automation = automated.sum() / len(df)
    false_positive_rate = np.logical_and(automated, ~correct).sum() / automated.sum()
    return accuracy, automation, false_positive_rate


def _get_row_prediction(row, non_automated_class, threshold):
    arg_max_int_index = row.argmax()
    arg_max_class = row.index[arg_max_int_index]
    label = arg_max_class[len("yhat_probs_"):]
    output = label if threshold < row[arg_max_int_index] else non_automated_class
    return output


def _determine_positive_binary_class(df, target, non_automated_class):
    labels = df[target].unique().tolist()
    labels.remove(non_automated_class)
    return labels[0]


def _get_yhat_probs_columns(df):
    yhat_probs_columns = [x for x in df.columns if x.startswith('yhat_probs_')]
    return yhat_probs_columns


def _compute_class_specific_automation_rate(predictions, target, cl, non_automated_class):
    label_is_class = predictions[target].eq(cl)
    automated = predictions[f'predicted_{target}'].ne(non_automated_class)
    label_is_class_and_automated = label_is_class & automated
    automation_rate = label_is_class_and_automated.sum() / label_is_class.sum()
    return automation_rate


def _compute_class_specific_automated_accuracy(predictions, target, cl, non_automated_class):
    automated_as_class = predictions[f'predicted_{target}'].eq(cl)
    label_is_class = predictions[target].eq(cl)
    automated_correctly_as_class = automated_as_class & label_is_class
    automated_accuracy = automated_correctly_as_class.sum() / automated_as_class.sum()
    return automated_accuracy


def _compute_automation_rate(predictions, target, non_automated_class):
    automated = predictions[f'predicted_{target}'].ne(non_automated_class)
    automation_rate = automated.sum() / len(predictions)
    return automation_rate


def _compute_automated_accuracy(predictions, target, non_automated_class):
    automated = predictions[f'predicted_{target}'].ne(non_automated_class)
    correct = predictions[f'predicted_{target}'].eq(predictions[target])
    automated_correctly = automated & correct
    automated_accuracy = automated_correctly.sum() / automated.sum()
    return automated_accuracy


def _get_results_for_thresholds(df_fit, df_test, calibration_data):
    is_binary = list(calibration_data.values())[0]['is_binary']
    results = {'calibration': {}, 'test': {}}
    if is_binary:
        non_automated_class = list(calibration_data.values())[0]['non_automated_class']
        positive_class = [cl for cl in list(calibration_data.values())[0]['all_classes']
                          if cl != non_automated_class][0]
        results = {'calibration': {}, 'test': {}}
        for df, key in zip([df_fit, df_test], ['calibration', 'test']):
            for target in calibration_data.keys():
                results[key][target] = {}
                scores = _score_prediction_binary(df, positive_class, target, calibration_data[target])
                results[key][target] = {
                    'automation_rate': scores[1],
                    'accuracy': scores[0]}
    else:
        results = {'calibration': {}, 'test': {}}
        predictions_using_thresholds = apply(df_fit.copy(), calibration_data)
        for df, key in zip([df_fit, df_test], ['calibration', 'test']):
            for target in calibration_data.keys():
                results[key][target] = {'class_specific': {}}
                non_automated_class = calibration_data[target]['non_automated_class']

                automation_rate = _compute_automation_rate(predictions_using_thresholds, target, non_automated_class)
                automated_accuracy = _compute_automated_accuracy(predictions_using_thresholds, target,
                                                                 non_automated_class)
                results[key][target]['automation_rate'] = automation_rate
                results[key][target]['automated_accuracy'] = automated_accuracy

                automated_classes = [cl for cl in calibration_data[target]['all_classes'] if cl != non_automated_class]
                for cl in automated_classes:
                    results[key][target]['class_specific'][cl] = {}
                    class_automation_rate = _compute_class_specific_automation_rate(predictions_using_thresholds,
                                                                                    target, cl, non_automated_class)
                    class_automated_accuracy = _compute_class_specific_automated_accuracy(predictions_using_thresholds,
                                                                                          target, cl,
                                                                                          non_automated_class)
                    results[key][target]['class_specific'][cl]['automation_rate'] = class_automation_rate
                    results[key][target]['class_specific'][cl]['automated_accuracy'] = class_automated_accuracy

    return results


def calibrate(df_fit, targets, target_accuracy, non_automated_class=None, important_classes=None,
              important_classes_strategy=ImportantClassesStrategy.max_yhat_in_important_classes):
    targets = targets if isinstance(targets, (list, tuple)) else [targets]
    if target_accuracy < 0 or target_accuracy > 1:
        raise Exception("Please set a target accuracy between 0 and 1.")
    if important_classes is None:
        important_classes = []
    elif isinstance(important_classes, str):
        important_classes = [important_classes]
    calibration_data = {}
    is_binary = 'yhat_probs' in df_fit.columns
    if is_binary and (non_automated_class is None or non_automated_class not in df_fit[targets[0]].unique()):
        raise ValueError('non_automated_class must be specified for binary classification problems and must be one'
                         'of the two classes observed in the target column.')
    non_automated_class = non_automated_class if non_automated_class is not None else NON_AUTOMATED_CLASS_DEFAULT
    for target in targets:
        baseline_accuracy = _compute_automated_accuracy(df_fit, target, non_automated_class)
        if target_accuracy < baseline_accuracy:
            warnings.warn(f'\nTarget accuracy specified ({target_accuracy}) is lower than the '
                          f'accuracy achieved before setting thresholds ({baseline_accuracy}) for target \'{target}\'.',
                          stacklevel=2)
        if is_binary:
            positive_class = _determine_positive_binary_class(df_fit, target, non_automated_class)
            threshold = _fit_threshold_for_label(df_fit, is_binary, positive_class,
                                                 target, target_accuracy)
            target_dtype = df_fit[target].dtype
            calibration_data[target] = {
                'important_classes': [],
                'important_thresholds': {},
                'generic_threshold': threshold,
                'important_classes_strategy': important_classes_strategy,
                'is_binary': True,
                'non_automated_class': non_automated_class,
                'all_classes': [positive_class, non_automated_class],
                'target_dtype': target_dtype,
                'target_accuracy': target_accuracy
            }

        else:
            labels = set(df_fit[target])
            if len(important_classes) > 0:
                calibration_data[target] = _compute_thresholds_on_label_basis(df_fit, target, target_accuracy,
                                                                              important_classes, non_automated_class,
                                                                              important_classes_strategy, labels)
            else:
                generic_threshold = _fit_threshold_for_multiple_labels(df_fit, target, target_accuracy,
                                                                       non_automated_class)
                target_dtype = df_fit[target].dtype
                calibration_data[target] = {
                    'important_classes': [],
                    'important_thresholds': {},
                    'generic_threshold': generic_threshold,
                    'important_classes_strategy': important_classes_strategy,
                    'is_binary': False,
                    'non_automated_class': non_automated_class,
                    'all_classes': list(labels),
                    'target_dtype': target_dtype,
                    'target_accuracy': target_accuracy
                }

    reference_predictions = apply(df_fit, calibration_data, in_place=False)
    for target in targets:
        automation_rate = _compute_automation_rate(reference_predictions, target, non_automated_class)
        if automation_rate < 0.01:
            warnings.warn(f'\nTarget accuracy specified ({target_accuracy}) results in an automation rate of '
                          f'{automation_rate} for target \'{target}\'. This is significantly low, you may want to '
                          f'choose a lower target accuracy.', stacklevel=2)

    return calibration_data


def apply(df, calibration_data, in_place=False):
    if in_place is False:
        df = df.copy()
    for target in calibration_data.keys():
        original_dtype_target = calibration_data[target]['target_dtype']
        is_binary = calibration_data[target]['is_binary']
        non_automated_class = calibration_data[target]['non_automated_class']
        important_classes = calibration_data[target]['important_classes']
        important_classes_strategy = calibration_data[target]['important_classes_strategy']

        df[f'predicted_{target}'] = non_automated_class

        if is_binary:
            classes = calibration_data[target]['all_classes']
            positive_class = [cl for cl in classes if cl != non_automated_class][0]
            positive_class_threshold = calibration_data[target]['generic_threshold']
            positive_class_series = pd.Series([positive_class] * len(df))
            df[f'predicted_{target}'] = positive_class_series.where(df['yhat_probs'].gt(positive_class_threshold),
                                                                    non_automated_class)
        else:
            yhat_probs_columns = _get_yhat_probs_columns(df)
            is_automated = pd.Series([False] * len(df), index=df.index)
            if important_classes_strategy == ImportantClassesStrategy.most_important_first:
                for important_class in important_classes:
                    non_automated = df[~is_automated]
                    yhat_probs = non_automated[f'yhat_probs_{important_class}']
                    threshold = calibration_data[target]['important_thresholds'][important_class]
                    is_class = pd.Series(data=yhat_probs > threshold, index=non_automated.index)
                    df.loc[is_class[is_class].index.values, f'predicted_{target}'] = important_class
                    yhat_probs_columns.remove(yhat_probs.name)
                    is_automated |= is_class

            elif important_classes_strategy == ImportantClassesStrategy.max_yhat_in_important_classes:
                meets_threshold = pd.DataFrame(data=[[False] * len(important_classes)] * len(df), index=df.index,
                                               columns=important_classes)
                for important_class in important_classes:
                    yhat_probs = df[f'yhat_probs_{important_class}']
                    threshold = calibration_data[target]['important_thresholds'][important_class]
                    is_class = yhat_probs > threshold
                    meets_threshold[important_class] = is_class
                    yhat_probs_columns.remove(yhat_probs.name)

                class_combinations = list(chain(
                    *[list(combinations(important_classes, k)) for k in range(1, len(important_classes) + 1)]))
                for combo in class_combinations:
                    classes = {x: (x in combo) for x in important_classes}
                    selected = pd.Series([True] * len(meets_threshold), index=df.index)
                    for k, v in classes.items():
                        selected &= meets_threshold[k] == v
                    if selected.sum() != 0:
                        combo_yhat_probs = df[selected][[f'yhat_probs_{x}' for x in combo]]
                        df.loc[selected, f'predicted_{target}'] = combo_yhat_probs.idxmax(axis=1).str.replace(
                            'yhat_probs_', '')
                        is_automated |= selected
            else:
                raise Exception('Unsupported important class strategy.')
            non_automated = df[~is_automated]
            if len(non_automated) != 0:
                threshold = calibration_data[target]['generic_threshold']
                maximal_yhat_probs = non_automated[yhat_probs_columns].max(axis=1)
                is_class = maximal_yhat_probs <= threshold
                df.loc[is_class[is_class].index.values, f'predicted_{target}'] = non_automated_class
                non_automated = non_automated[~is_class]
                if len(non_automated) != 0:
                    important_classes_yhat_probs_columns = {f'yhat_probs_{_class}' for _class in important_classes}
                    non_important_yhat_probs_columns = list(set(yhat_probs_columns).difference(important_classes_yhat_probs_columns))
                    if len(non_important_yhat_probs_columns) != 0:
                        df.loc[non_automated.index.values, f'predicted_{target}'] = non_automated[non_important_yhat_probs_columns].idxmax(axis=1).str.replace('yhat_probs_', '')

        try:
            df[f'predicted_{target}'] = df[f'predicted_{target}'].astype(original_dtype_target)
        except ValueError:
            pass
    return df


def score(df, calibration_data):
    output_dict = {}
    for target, data in calibration_data.items():
        actual = df[target]
        predicted = df[f'predicted_{target}']

        classes = data['all_classes']
        non_automated_class = data['non_automated_class']

        automated_classes = [_class for _class in classes if _class != non_automated_class]

        automation_accuracy_data = {}

        target_results_dict = {'target_accuracy': data['target_accuracy'],
                               'automation_overall': {},
                               'automation_per_class': {},
                               'f1_for_automated_rows':
                                   {'weighted_average': {},
                                    'classes': {}
                                    },
                               'f1_for_all_rows':
                                   {'weighted_average': {},
                                    'classes': {}
                                    }}

        automated_rows = df[df[f'predicted_{target}'].ne(non_automated_class)]
        automated_actual = automated_rows[target]
        automated_predicted = automated_rows[f'predicted_{target}']

        overall_automation_rate = _compute_automation_rate(df, target, non_automated_class)
        overall_accuracy = _compute_automated_accuracy(df, target, non_automated_class)

        overall_automated_precision = precision_score(automated_rows[target], automated_rows[f'predicted_{target}'],
                                                      average='weighted')
        overall_automated_recall = recall_score(automated_rows[target], automated_rows[f'predicted_{target}'],
                                                average='weighted')
        overall_automated_f1 = f1_score(automated_rows[target], automated_rows[f'predicted_{target}'],
                                        average='weighted')
        overall_automated_count = len(automated_actual)

        overall_precision = precision_score(df[target], df[f'predicted_{target}'],
                                            average='weighted')
        overall_recall = recall_score(df[target], df[f'predicted_{target}'],
                                      average='weighted')
        overall_f1 = f1_score(df[target], df[f'predicted_{target}'], average='weighted')
        overall_count = len(df)

        automation_accuracy_data['Overall'] = {
            'automation_rate': overall_automation_rate,
            'accuracy': overall_accuracy
        }

        target_results_dict['automation_overall']['automation'] = overall_automation_rate
        target_results_dict['automation_overall']['accuracy'] = overall_accuracy
        target_results_dict['automation_overall']['for_review'] = 1 - overall_automation_rate

        target_results_dict['f1_for_automated_rows']['weighted_average']['precision'] = overall_automated_precision
        target_results_dict['f1_for_automated_rows']['weighted_average']['recall'] = overall_automated_recall
        target_results_dict['f1_for_automated_rows']['weighted_average']['f1_score'] = overall_automated_f1
        target_results_dict['f1_for_automated_rows']['weighted_average']['count'] = overall_automated_count

        target_results_dict['f1_for_all_rows']['weighted_average']['precision'] = overall_precision
        target_results_dict['f1_for_all_rows']['weighted_average']['recall'] = overall_recall
        target_results_dict['f1_for_all_rows']['weighted_average']['f1_score'] = overall_f1
        target_results_dict['f1_for_all_rows']['weighted_average']['count'] = overall_count

        for _class in automated_classes:
            class_automation_rate = _compute_class_specific_automation_rate(df, target, _class, non_automated_class)
            class_accuracy = _compute_class_specific_automated_accuracy(df, target, _class, non_automated_class)
            automation_accuracy_data[_class] = {
                'automation_rate': class_automation_rate,
                'accuracy': class_accuracy
            }
            target_results_dict['automation_per_class'][_class] = {}
            target_results_dict['automation_per_class'][_class]['automation'] = class_automation_rate
            target_results_dict['automation_per_class'][_class]['accuracy'] = class_accuracy
            target_results_dict['automation_per_class'][_class]['for_review'] = 1 - class_automation_rate

            automated_class_precision = precision_score(automated_actual, automated_predicted, labels=[_class],
                                                        average='weighted')
            automated_class_recall = recall_score(automated_actual, automated_predicted, labels=[_class],
                                                  average='weighted')
            automated_class_f1 = f1_score(automated_actual, automated_predicted, labels=[_class], average='weighted')
            automated_class_count = automated_actual.eq(_class).sum()

            target_results_dict['f1_for_automated_rows']['classes'][_class] = {}
            target_results_dict['f1_for_automated_rows']['classes'][_class]['precision'] = automated_class_precision
            target_results_dict['f1_for_automated_rows']['classes'][_class]['recall'] = automated_class_recall
            target_results_dict['f1_for_automated_rows']['classes'][_class]['f1_score'] = automated_class_f1
            target_results_dict['f1_for_automated_rows']['classes'][_class]['count'] = automated_class_count

            class_precision = precision_score(actual, predicted, labels=[_class], average='weighted')
            class_recall = recall_score(actual, predicted, labels=[_class], average='weighted')
            class_f1 = f1_score(actual, predicted, labels=[_class], average='weighted')
            class_count = actual.eq(_class).sum()

            target_results_dict['f1_for_all_rows']['classes'][_class] = {}
            target_results_dict['f1_for_all_rows']['classes'][_class]['precision'] = class_precision
            target_results_dict['f1_for_all_rows']['classes'][_class]['recall'] = class_recall
            target_results_dict['f1_for_all_rows']['classes'][_class]['f1_score'] = class_f1
            target_results_dict['f1_for_all_rows']['classes'][_class]['count'] = class_count

        non_automated_class_precision = precision_score(actual, predicted, labels=[non_automated_class],
                                                        average='weighted')
        non_automated_class_recall = recall_score(actual, predicted, labels=[non_automated_class], average='weighted')
        non_automated_class_f1 = f1_score(actual, predicted, labels=[non_automated_class], average='weighted')
        non_automated_class_count = actual.eq(non_automated_class).sum()

        target_results_dict['f1_for_all_rows']['classes'][non_automated_class] = {}
        target_results_dict['f1_for_all_rows']['classes'][non_automated_class][
            'precision'] = non_automated_class_precision
        target_results_dict['f1_for_all_rows']['classes'][non_automated_class]['recall'] = non_automated_class_recall
        target_results_dict['f1_for_all_rows']['classes'][non_automated_class]['f1_score'] = non_automated_class_f1
        target_results_dict['f1_for_all_rows']['classes'][non_automated_class]['count'] = non_automated_class_count

        automation_accuracy_report = pd.DataFrame(automation_accuracy_data).T
        automation_accuracy_report_string = repr(automation_accuracy_report)
        report_string_lines = automation_accuracy_report_string.split('\n')
        formatted_overall_line = colorama.Fore.CYAN + report_string_lines[1] + colorama.Style.RESET_ALL
        formatted_report = '\n'.join([report_string_lines[0], formatted_overall_line] + report_string_lines[2:])
        print_info(formatted_report)

        f1_table_data = {**{'Overall': target_results_dict['f1_for_automated_rows']['weighted_average']},
                         **target_results_dict['f1_for_automated_rows']['classes']}
        f1_table = pd.DataFrame(f1_table_data).T
        rows = repr(f1_table).split('\n')
        overall_row = rows[1]
        formatted_overall_row = colorama.Fore.CYAN + overall_row + colorama.Style.RESET_ALL
        formatted_f1_table = '\n'.join([rows[0], formatted_overall_row] + rows[2:])
        print_info(formatted_f1_table)

        output_dict[target] = target_results_dict

    return output_dict
