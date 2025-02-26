import os
import logging
from pathlib import Path
from flask import Flask

from kortical.environment import get_environment_name

from module_placeholder.logging import logging_config
from module_placeholder.api import endpoints
from module_placeholder.ui import index

logging_config.init()

logger = logging.getLogger(__name__)


def create_app():
    current_dir = os.path.dirname(__file__)
    static_path = os.path.join(Path(current_dir), 'ui', 'static')
    flask_app = Flask(__name__, static_url_path='/static', static_folder=static_path)
    flask_app.config['SECRET_KEY'] = 'flask_key_placeholder'
    flask_app.config['SESSION_COOKIE_NAME'] = f'module_placeholder_{get_environment_name()}_session'
    flask_app.config['SESSION_COOKIE_PATH'] = "/"
    endpoints.register_routes(flask_app)
    index.register_routes(flask_app)
    return flask_app


app = create_app()
