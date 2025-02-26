import logging
from flask import request
from kortical.app import get_app_config

app_config = get_app_config(format='yaml')
api_key = app_config['api_key']
logger = logging.getLogger(__name__)


def validate_authentication():
    valid, api_key = _validate_api_key(request)
    return valid, api_key


def _validate_api_key(req):
    logger.info("Validating API key")
    # Support providing the api key in the following ways: api_key in an arg or in a form, or Api-Key as a header or cookie.
    api_key_from_request = req.args.get('api_key')
    if api_key_from_request is None:
        api_key_from_request = req.form.get('api_key')
        if api_key_from_request is None:
            api_key_from_request = req.headers.get('Api-Key')
            if api_key_from_request is None:
                api_key_from_request = req.cookies.get('api_key')
                if api_key_from_request is None:
                    logger.info("No api key was found.")
                    return False, None

    if api_key_from_request.lower() != api_key.lower():
        # do not show valid_api_key in this message as it will become the actual response
        logger.warning(f"The api_key in the request '{api_key_from_request}' is invalid.")
        return False, None

    return True, api_key
