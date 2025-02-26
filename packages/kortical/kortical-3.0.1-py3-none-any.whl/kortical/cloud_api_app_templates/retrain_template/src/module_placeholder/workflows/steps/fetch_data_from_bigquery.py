from sklearn.model_selection import train_test_split

from module_placeholder.bigquery.bigquery import get_dataframe_from_bigquery


class FetchDataFromBigquery:

    def execute(self, data, progress_report_function):
        progress_report_function('Fetching latest train/test data from Bigquery...')

        df = get_dataframe_from_bigquery()
        df_train, df_test = train_test_split(df, train_size=0.8, random_state=0)

        data['df_train'] = df_train
        data['df_test'] = df_test

        return data
