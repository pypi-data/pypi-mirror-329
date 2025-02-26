import logging
import sys
import os
from celery import Celery

from kortical.api.component_instance import ComponentInstance
from kortical.api.environment import Environment
from kortical.api.project import Project
from kortical.app import is_running_in_cloud


logger = logging.getLogger(__name__)
celery = None


def make_celery(app):
    redis_port = os.getenv('REDIS_PORT', '6379')
    global celery
    if not is_running_in_cloud():
        logger.info(f"Setting local redis urls for celery.")
        broker_url = result_backend = f'redis://localhost:{redis_port}'
    else:
        project = Project.get_selected_project()
        environment = Environment.get_selected_environment(project)
        redis_instance = ComponentInstance.get_component_instance(project, environment, 'celery_redis')
        redis_service_name = redis_instance.get_kubernetes_name()
        logger.info(f"Setting remote [{redis_service_name}] redis urls for celery.")
        broker_url=f'redis://{redis_service_name}:6379',
        result_backend=f'redis://{redis_service_name}:6379'
    logger.info(f"Creating celery: result backend [{result_backend}], broker url [{broker_url}]")
    celery = Celery(
        app.import_name,
        backend=result_backend,
        broker=broker_url
    )
    logger.info("Celery in")
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask


print(f"Before if celery in [{sys.argv}] worker in [{sys.argv[0]}] [{'celery' in sys.argv[0]}] [{'worker' in sys.argv}]")
if "celery" in sys.argv[0] and "worker" in sys.argv:
    import module_placeholder.main

    print(f"After if celery")
