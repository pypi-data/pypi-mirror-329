import inspect
import os
import pandas as pd
from shutil import copyfile

module_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
example_datasets = ['bbc',
                    'customer_reviews',
                    'delhi_climate',
                    'enron',
                    'enron_multi_label',
                    'house_price_regression',
                    'iris',
                    'margin',
                    'stock_prices',
                    'titanic']


def load(name):

    if name in example_datasets:
        path = os.path.join(module_directory, f'{name}.csv')
    else:
        raise Exception(f'Invalid argument [{name}]. Please select one from the following:\n{example_datasets}')

    return pd.read_csv(path)


def write_to_disk(name, path=None):

    if not path:
        path = os.path.join(os.getcwd(), f'{name}.csv')

    if name in example_datasets:
        copyfile(os.path.join(module_directory, f'{name}.csv'), path)
    else:
        raise Exception(f'Invalid argument. Please select one from the following:\n{example_datasets}')
