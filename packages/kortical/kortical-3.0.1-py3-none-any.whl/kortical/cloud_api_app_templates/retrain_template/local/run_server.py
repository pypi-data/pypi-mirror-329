import logging
import subprocess
from module_placeholder.logging import logging_config
from kortical.app import get_app_config
from local.docker_image_run import DockerImageRun

logging_config.init()
logger = logging.getLogger(__name__)

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']

if __name__ == '__main__':
    port = 5001
    print(f"Paste the following into your browser to access the app:\n\n[http://127.0.0.1:{port}?api_key={api_key}]")

    # start celery worker as a subprocess
    celery_worker = subprocess.Popen(['celery', '-A', 'module_placeholder.celery', 'worker', '--loglevel=info'])

    with DockerImageRun('redis:latest', ports={'6379/tcp': 6379}):
        try:
            import module_placeholder.main
            module_placeholder.main.app.run(debug=False, port=port)
        finally:
            # ensure the celery worker process is terminated when the app is done running
            celery_worker.terminate()
