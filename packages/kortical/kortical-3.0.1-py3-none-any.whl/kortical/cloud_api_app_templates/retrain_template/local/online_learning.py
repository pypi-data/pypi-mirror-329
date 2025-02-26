import os

from kortical.app import requests, get_app_config
from kortical.api.enums import ComponentType

from module_placeholder.helpers.root_dir import from_root_dir


app_config = get_app_config(format='yaml')
api_key = app_config['api_key']

DATA_PATH = from_root_dir(os.path.join('data', 'dataset_2.csv'))

if __name__ == '__main__':

    with open(DATA_PATH) as f:
        file = f.read()
    response = requests.post(component_name='module_placeholder',
                             component_type=ComponentType.APP,
                             url=f'/online_learning?api_key={api_key}',
                             files={'file': file})
    train_id = response.json()
