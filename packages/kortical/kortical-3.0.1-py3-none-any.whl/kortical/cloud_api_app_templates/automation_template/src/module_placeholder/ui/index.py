import os
import flask
import logging
from module_placeholder.ui import jinja
from module_placeholder.authentication import safe_api_call
from kortical.app import get_app_config

logger = logging.getLogger(__name__)

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']
# Adjust base name depending on environment
app_name = "" if os.environ.get('SERVER_RUNNING_LOCALLY', "FALSE") == "TRUE" else "app_name_placeholder"


def register_routes(app):

    @app.route('/', methods=['get'])
    @safe_api_call
    def get_index():
        template = jinja.get_template('index.html')
        return flask.Response(template.render(api_key=api_key, app_name=app_name))
