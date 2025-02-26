from kortical.api import _api, code, data, experiment_framework, model, superhuman_calibration


def init(system_url=None, credentials=None):
    return _api.init(system_url, credentials)


def get(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.get(url, *args, **kwargs)


def put(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.put(url, *args, **kwargs)


def head(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.head(url, *args, **kwargs)


def post(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.post(url, *args, **kwargs)


def patch(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.patch(url, *args, **kwargs)


def delete(url, *args, throw=True, **kwargs):
    kwargs['throw'] = throw
    return _api.delete(url, *args, **kwargs)


def post_file(url, fields, filename, filepath, *args, description=None, throw=True, **kwargs):
    kwargs['throw'] = throw
    kwargs['description'] = description
    return _api.post_file(url, fields, filename, filepath, *args, **kwargs)


def get_project_url():
    return _api._get_project_url()
