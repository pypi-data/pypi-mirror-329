import pickle
import pandas as pd
import numpy as np
from kortical.data_flow.nodes import custom_node


class Thresholds(custom_node.CustomNode):

    def __init__(self, kortical_url, thresholds_id, data_source_fit, data_source_test, targets, target_accuracy, non_automated_class=None, name=None):
        super().__init__(f"thresholds: {thresholds_id}" if name is None else name, [data_source_fit, data_source_test], thresholds_id, targets, target_accuracy, non_automated_class)
        self.url = kortical_url
        self.thresholds_id = thresholds_id
        self.data_source_fit = data_source_fit
        self.data_source_test = data_source_test
        self.targets = targets if isinstance(targets, (list, tuple)) else [targets]
        self.target_accuracy = target_accuracy
        self.non_automated_class = non_automated_class

        # we don't actually use the API but we ensure they have valid credentials
        #kortical.api.init(self.url)

    def _execute(self, data):
        df_fit = data[self.data_source_fit][0]
        df_test = data[self.data_source_test][0]

        thresholds = {}
        for target in self.targets:
            labels = set(df_fit[target].unique())
            labels.union(df_test[target].unique())
            is_binary = 'yhat_probs' in df_test.columns
            if is_binary:
                labels = [self._find_positive_binary_class(df_fit, target)]

            if is_binary:
                thresholds[target] = self._fit_per_label_thresholds_for_automated_accuracy(df_fit, is_binary, labels, target, self.target_accuracy)
                self._score_prediction_binary(df_fit, labels, target, thresholds[target])
                self._score_prediction_binary(df_test, labels, target, thresholds[target])
            else:
                yhat_probs_columns = [x for x in df_fit.columns if x.startswith('yhat_probs_')]
                thresholds[target] = self._fit_multi_class_thresholds_for_automated_accuracy(df_fit, yhat_probs_columns, target, self.target_accuracy, self.non_automated_class)
                self.score_prediction_multi_class(df_fit, yhat_probs_columns, target, thresholds[target], self.non_automated_class)
                self.score_prediction_multi_class(df_test, yhat_probs_columns, target, thresholds[target], self.non_automated_class)

        # store thresholds against threshold_id. Move to cloud storage but need to resolve credentials thing
        with open(f'thresholds_{self.thresholds_id}', 'wb') as f:
            pickle.dump(thresholds, f, protocol=pickle.HIGHEST_PROTOCOL)

        return {'thresholds': thresholds}

    def _fit_per_label_thresholds_for_automated_accuracy(self, df, is_binary, labels, target, target_accuracy):
        thresholds = {l: 0.5 for l in labels}
        for l in labels:
            percentage_right, _, _ = self._score_label_for_positive_class(df, is_binary, l, target, thresholds[l])
            distance = 0.25
            for i in range(12):
                up_percentage_right, _, _ = self._score_label_for_positive_class(df, is_binary, l, target, thresholds[l] + distance)
                down_percentage_right, _, _ = self._score_label_for_positive_class(df, is_binary, l, target, thresholds[l] - distance)
                if abs(target_accuracy - percentage_right) >= abs(target_accuracy - up_percentage_right) and percentage_right != 1.0:
                    thresholds[l] += distance
                    percentage_right = up_percentage_right
                elif abs(target_accuracy - percentage_right) >= abs(target_accuracy - down_percentage_right):
                    thresholds[l] -= distance
                    percentage_right = down_percentage_right
                distance *= 0.5
        return thresholds

    def _fit_multi_class_thresholds_for_automated_accuracy(self, df, yhat_probs_columns, target, target_accuracy, non_automated_class):
        threshold = 0.5
        percentage_right, _, _ = self.score_prediction_multi_class(df, yhat_probs_columns, target, threshold, non_automated_class)
        distance = 0.25
        for i in range(12):
            up_percentage_right, _, _ = self.score_prediction_multi_class(df, yhat_probs_columns, target, threshold + distance, non_automated_class)
            down_percentage_right, _, _ = self.score_prediction_multi_class(df, yhat_probs_columns, target, threshold - distance, non_automated_class)
            if abs(target_accuracy - percentage_right) >= abs(target_accuracy - up_percentage_right) and percentage_right != 1.0:
                threshold += distance
                percentage_right = up_percentage_right
            elif abs(target_accuracy - percentage_right) >= abs(target_accuracy - down_percentage_right):
                threshold -= distance
                percentage_right = down_percentage_right
            distance *= 0.5
        return threshold

    def _score_label_for_positive_class(self, df, is_binary, l, target, threshold):
        # find where there were labels then percentage of positives that were right
        # find right as a proportion of all correct
        # find correct as a percentage of total dataset
        if is_binary:
            is_label = df[target] == l
            df['temp'] = df[f"yhat_probs"] > threshold
        else:
            is_label = df[l] == 1.0
            df['temp'] = df[f"yhat_probs_{l}"] > threshold
        num_predicted_positive = df['temp'].sum()
        df['temp'] = np.logical_and(is_label, df['temp'])
        num_positives_correct = df['temp'].sum()
        num_positives = is_label.sum()
        num_possible = len(df)
        percentage_right = num_positives_correct / num_predicted_positive if num_predicted_positive != 0 else 0
        percentage_found = num_positives_correct / num_positives
        percentage_found_of_possible = num_positives_correct / num_possible
        print(f"{l} {threshold}: {percentage_right}, {percentage_found}, {percentage_found_of_possible}")
        return percentage_right, percentage_found, percentage_found_of_possible

    @staticmethod
    def _score_prediction_binary(df, labels, target, thresholds):
        is_label = df[target] == labels[0]
        predicted = df[f"yhat_probs"] > thresholds[labels[0]]
        num_predicted_positive = predicted.sum()
        correct = predicted == is_label
        correct_when_label = correct[predicted]
        num_positives_correct = correct_when_label.sum()
        accuracy = num_positives_correct / len(correct_when_label)
        automation = num_predicted_positive / len(df)
        false_positive_rate = (num_predicted_positive - num_positives_correct) / num_predicted_positive
        print(f"Percentage right [{accuracy*100:.3f}%], False Positives [{false_positive_rate*100:.3f}%], Automation [{automation*100:.3f}%]")
        return accuracy, automation, false_positive_rate

    @staticmethod
    def score_prediction_multi_class(df, yhat_probs_columns, target, threshold, non_automated_class=None):
        df = df.reset_index()
        if non_automated_class is None:
            non_automated_class = '$$Not Specified$$'
        df_len = len(df)
        _class = pd.Series([None] * df_len)

        for i, row in df[yhat_probs_columns].iterrows():
            # index = np.argmax(row)
            arg_max_int_index = np.argmax(row)
            arg_max_class = row.index[arg_max_int_index]
            label = arg_max_class[len("yhat_probs_"):]
            c = label if threshold < row[arg_max_int_index] else non_automated_class
            _class[i] = c
        correct = df[target] == _class
        automated = _class != non_automated_class
        correct_when_label = correct[automated]
        accuracy = correct_when_label.sum() / len(correct_when_label)
        automation = automated.sum() / len(df)
        false_positive_rate = np.logical_and(automated, ~correct).sum() / automated.sum()
        print(f"Threshold: [{threshold}], Percentage right [{accuracy*100:.3f}%], False Positives [{false_positive_rate*100:.3f}%], Automation [{automation*100:.3f}%]")
        return accuracy, automation, false_positive_rate

    @staticmethod
    def _find_positive_binary_class(df, target):
        high_probabilities_dominant_percentage = (df['yhat_probs'] > 0.5).sum() / len(df)
        vc = df[target].value_counts()
        return vc.index[int(high_probabilities_dominant_percentage <= 0.5)]