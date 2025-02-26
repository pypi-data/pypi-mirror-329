import time

from kortical.app import requests, get_app_config
from kortical.api.enums import ComponentType


app_config = get_app_config(format='yaml')
api_key = app_config['api_key']


if __name__ == '__main__':

    response = requests.post(component_name='module_placeholder', component_type=ComponentType.APP, url=f'/train?api_key={api_key}')
    train_id = response.json()['train_id']
    train_status = ''

    while "complete" not in train_status:
        response = requests.get(component_name='module_placeholder', component_type=ComponentType.APP, url=f'/train/{train_id}?api_key={api_key}')
        print(response.json())
        train_status = response.json()['status']
        time.sleep(2)
