import functools
from inspect import getcallargs


DEFAULT_NAMESPACE = 'default'


def clean_namespace(func):
    @functools.wraps(func)
    def _clean_namespace(*args, **kwargs):

        call_args = getcallargs(func, *args, **kwargs)
        namespace = call_args.get('namespace')
        if namespace is not None:
            call_args['namespace'] = namespace.strip('/')
            return func(**call_args)
        else:
            raise TypeError(f'Decorated function {func.__name__} does not have "namespace" in its signature.')

    return _clean_namespace
