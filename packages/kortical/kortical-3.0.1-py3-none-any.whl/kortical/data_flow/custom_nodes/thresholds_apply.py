import pickle
import pandas as pd
import numpy as np
from kortical.data_flow.nodes import custom_node


class ApplyThresholds(custom_node.CustomNode):

    def __init__(self, kortical_url, thresholds_id, data_source, targets, non_automated_class=None, name=None):
        super().__init__(f"thresholds: {thresholds_id}" if name is None else name, [data_source], thresholds_id, targets, non_automated_class)
        self.url = kortical_url
        self.thresholds_id = thresholds_id
        self.data_source = data_source
        self.targets = targets if isinstance(targets, (list, tuple)) else [targets]
        self.non_automated_class = non_automated_class

    def _execute(self, data):
        df = data[self.data_source][0]
        is_binary = 'yhat_probs' in df.columns

        with open(f'thresholds_{self.thresholds_id}', 'rb') as f:
            thresholds = pickle.load(f)

        for target in self.targets:
            if is_binary:
                for k, v in thresholds[target].items():
                    df.loc[(df[f'predicted_{target}'] == k) & (df['yhat_probs'] < v), f'predicted_{target}'] = self.non_automated_class
            else:
                df_len = len(df)
                yhat_probs_columns = [x for x in df.columns if x.startswith('yhat_probs_')]
                _class = pd.Series([None] * df_len)

                for i, row in df[yhat_probs_columns].iterrows():
                    index = row.argmax()
                    label = row.index[index].replace('yhat_probs_', '')
                    c = label if thresholds[target] < row[index] else self.non_automated_class
                    df.loc[i, f'predicted_{target}'] = c


        return {self.data_source: df, 'thresholds': thresholds}