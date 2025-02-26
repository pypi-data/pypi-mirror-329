import docker
import os
import pytest

import subprocess

LOCAL_ENVIRONMENT = False


@pytest.fixture(scope='session')
def app():

    docker_client = docker.from_env()
    # run the redis container, letting Docker choose a random free port, so we can run concurrent tests
    redis_container = docker_client.containers.run('redis:latest', ports={'6379/tcp': None}, detach=True)
    # query Docker for the port that was assigned
    redis_info = docker_client.api.inspect_container(redis_container.id)
    redis_port = redis_info['NetworkSettings']['Ports']['6379/tcp'][0]['HostPort']
    os.environ['REDIS_PORT'] = str(redis_port)
    celery_worker = subprocess.Popen(['celery', '-A', 'module_placeholder.celery', 'worker', '--loglevel=info'])
    os.environ['TESTING'] = "true"

    try:
        from module_placeholder import main
        flask_app = main.app
        flask_app.config['TESTING'] = True
        # flask_app.config['REDIS_URL'] = f'redis://localhost:{redis_port}'
        yield flask_app
    finally:
        # ensure the celery worker process is terminated when the app is done running
        celery_worker.terminate()
        redis_container.stop()
