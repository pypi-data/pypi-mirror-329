import os
import flask
import logging
from kortical import app

from module_placeholder.ui import jinja
from module_placeholder.authentication import safe_api_call

logger = logging.getLogger(__name__)

app_config = app.get_app_config(format='yaml')
app_title = app_config['app_title']
app_title_extension = app_config.get('app_title_extension', '')
logo_image_url = app_config['logo_image_url']

environment_config = {}

# Adjust base name depending on environment
app_name = "" if os.environ.get('SERVER_RUNNING_LOCALLY', "FALSE") == "TRUE" else "module_placeholder"


def register_routes(app):

    @app.route('/', methods=['get'])
    @safe_api_call
    def get_index():
        template = jinja.get_template('index.html')
        return flask.Response(template.render(
            app_name=app_name,
            app_title=app_title,
            app_title_extension=app_title_extension,
            logo_image_url=logo_image_url))
