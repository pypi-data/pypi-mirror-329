from urllib.parse import quote

from kortical import api


def upload_data(file_name, file_stream):
    file_stream.seek(0)
    files = {'file': (file_name, file_stream, 'text/csv')}
    response = api.post('/api/v1/data', files=files)
    return response.json()['data_id']


def create_report(data_id):
    json = {'data_id': data_id}
    response = api.post('/data/insights/report', json=json)
    return response.json()['report_id']


def set_targets(data_id, targets):
    if not isinstance(targets, (list, tuple)):
        targets = [targets]
    api.post(f"/api/v1/data/{data_id}/targets", json=targets)


def get_column(data_id, column_name):
    response = api.get(f"/api/v1/data/{data_id}/column?column={quote(column_name)}")
    return response.json()['column']


def generate_code(data_id):
    response = api.get(f'/api/v1/data/{data_id}/code')
    return response.json()['code']


def validate_code(data_id, code):
    data = {'specification': code}
    response = api.patch(f'/api/v1/data/{data_id}/code/validate', data=data)
    return response.json()['errors']
