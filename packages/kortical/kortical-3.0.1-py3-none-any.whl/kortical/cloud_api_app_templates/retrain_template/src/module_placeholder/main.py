import os
import logging
from pathlib import Path

import kortical.app
from flask import Flask, Response

from kortical.environment import get_environment_name

from module_placeholder.logging import logging_config
from module_placeholder.celery import make_celery

app_config = kortical.app.get_app_config(format='yaml')
logging_config.init(log_level=app_config.get('log_level', 20))

logger = logging.getLogger(__name__)


def create_app():
    current_dir = os.path.dirname(__file__)
    static_path = os.path.join(Path(current_dir), 'ui', 'static')
    templates_path = os.path.join(Path(current_dir), 'templates')
    logger.info(f"Loading templates from {templates_path}")
    flask_app = Flask(__name__, static_url_path='/static', static_folder=static_path, template_folder=templates_path)
    flask_app.config['SECRET_KEY'] = 'flask_key_placeholder'
    flask_app.config['SESSION_COOKIE_NAME'] = f'module_placeholder_{get_environment_name()}_session'
    flask_app.config['SESSION_COOKIE_PATH'] = "/"

    # set up celery
    make_celery(flask_app)

    # Some routes use celery so we import and register them after.
    from module_placeholder.api.endpoints import register_routes
    from module_placeholder.ui import index
    register_routes(flask_app)
    index.register_routes(flask_app)
    return flask_app


app = create_app()
