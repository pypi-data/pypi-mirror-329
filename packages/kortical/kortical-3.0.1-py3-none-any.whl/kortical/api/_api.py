from cryptography.fernet import InvalidToken
from datetime import datetime, timedelta
from io import IOBase
import os
from pathlib import Path
import time
from urllib.parse import urlparse
from urllib3.exceptions import NewConnectionError, SSLError
import requests
from requests_toolbelt import MultipartEncoder, MultipartEncoderMonitor
import shutil
from tqdm import tqdm

from kortical.helpers import is_interactive
from kortical.cloud import _random_seed
from kortical.config import kortical_config
from kortical.cloud.cloud import IS_KUBERNETES_ENVIRONMENT

from kortical.helpers.encryption_helpers import decrypt
from kortical.helpers.exceptions import KorticalKnownException
from kortical.helpers.print_helpers import print_error, print_info, print_success, print_question, print_warning, format_warning


project_url = None
website_url = None
email = None
password = None
LOGIN_TIMEOUT = 5

session = requests.session()


# def is_kortical_user_on_prod_platform(email, url):
#     return "@kortical.com" in email and "platform.test.kortical.com" not in url and not url.startswith('https://platform.kortical.com/kortical/demo')
#
#
# def active_recently(seconds=300):
#     active = False
#
#     last_time_active = kortical_config.get("time_of_last_api_call", force_global=True)
#     if last_time_active is not None:
#         # Measure time since last cli command
#         time_elapsed = datetime.now() - datetime.fromisoformat(last_time_active)
#         if time_elapsed < timedelta(seconds=seconds):
#             active = True
#
#     # Update with current time
#     kortical_config.set("time_of_last_api_call", datetime.now().isoformat(), force_global=True, print=False)
#
#     return active


def init(url, encrypted_credentials):
    global project_url
    global website_url
    global email
    global password

    url = kortical_config.clean_url(url)

    # If no inputs, read saved config from kubernetes...
    if IS_KUBERNETES_ENVIRONMENT:
        url = os.environ['KORE_SYSTEM_URL']
        email = os.environ['SERVICE_ACCOUNT_EMAIL']
        password = os.environ.get('SERVICE_ACCOUNT_SECRET')
        if password is None:
            password = os.environ.get('SERVICE_ACCOUNT_PASSWORD')
            if password is None:
                raise Exception('Credentials for Kortical were not found.')
        encrypted_credentials = {
            'email': email,
            'password': password
        }
    # ... or saved config
    else:
        if url is None:
            url = kortical_config.get('system_url')
        if encrypted_credentials is None:
            encrypted_credentials = kortical_config.get('credentials')
            # Test we can decrypt the credentials or unset them
            try:
                if encrypted_credentials:
                    decrypt(encrypted_credentials, key=_random_seed)
            except InvalidToken:
                encrypted_credentials = None

        # If no saved config either, launch user prompts
        url, encrypted_credentials = _user_prompt_and_complete_config(url, encrypted_credentials)

    # Do the actual init
    if 'email' not in encrypted_credentials:
        credentials = decrypt(encrypted_credentials, key=_random_seed)
    else:
        credentials = encrypted_credentials
    email = credentials['email']
    password = credentials['password']
    _set_url(url)
    try:
        _login()
    except KorticalKnownException:
        raise
    except SSLError:
        raise KorticalKnownException(
            "We were unable to log you in. It looks like there maybe a firewall or proxy issue blokcing your requests to the platform. If you are unsure how to proceed, please contact the Kortical team for assistance on slack (fastest response times) or email support@kortical.com")
    except Exception:
        raise KorticalKnownException(
            "We were unable to log you in. Please check the system URL is correct and that you can log into the platform. If you are unsure how to proceed, please contact the Kortical team for assistance on slack (fastest response times) or email support@kortical.com")

    if kortical_config.use_memory_config:
        kortical_config._set_in_memory('system_url', url)
        kortical_config._set_in_memory('credentials', encrypted_credentials)


def _get_website_url():
    return website_url


def _get_project_url():
    return project_url


def get(url, *args, throw=True, **kwargs):
    global session
    return _web_call(session.get, url, *args, throw=throw, **kwargs)


def post(url, *args, throw=True, **kwargs):
    global session
    return _web_call(session.post, url, *args, throw=throw, **kwargs)


def patch(url, *args, throw=True, **kwargs):
    global session
    return _web_call(session.patch, url, *args, throw=throw, **kwargs)


def put(url, *args, throw=True, **kwargs):
    global session
    return _web_call(session.put, url, *args, throw=throw, **kwargs)


def head(url, *args, throw=True, **kwargs):
    global session
    return _web_call(session.head, url, *args, throw=throw, **kwargs)


def delete(url, *args, throw=True, **kwargs):
    global session
    return _web_call(session.delete, url, *args, throw=throw, **kwargs)


def post_file(url, fields, filename, filepath, *args, description=None, throw=True, **kwargs):
    path = Path(filepath)
    total_size = path.stat().st_size
    if description is None:
        description = filename

    print_info("Uploading and processing file.")
    with tqdm(
            desc=description,
            total=total_size,
            unit="B",
            unit_scale=True,
            unit_divisor=1024,
    ) as bar:
        file_upload_complete = False

        def upload_file_progress_callback(m):
            nonlocal file_upload_complete
            bar.update(m.bytes_read - bar.n)
            if m.encoder.finished and not file_upload_complete:
                bar.close()
                file_upload_complete = True
                print_success("Finished Uploading to Kortical, we are now processing your file, "
                              "this may take some time please bear with us.")

        with open(filepath, "rb") as f:
            fields[filename] = (filename, f)
            encoder = MultipartEncoder(fields=fields)
            monitor = MultipartEncoderMonitor(
                encoder, upload_file_progress_callback
            )
            request_headers = {
                'Content-Type': encoder.content_type
            }

            global session
            return _web_call(session.post, url, *args, throw=throw, data=monitor, headers=request_headers, **kwargs)


def _web_call(function, url, *args, throw=True, **kwargs):

    num_retries = 5
    retry_index = 0
    back_off_seconds = 4
    response = None

    if _get_project_url() is None:
        init(None, None)

    url = _get_project_url() + url
    while not response:
        try:
            response = function(url, *args, **kwargs)
            if response.status_code == 401 or response.status_code == 403:
                raise ConnectionRefusedError("We were unable to log you in. Please check the system URL is correct "
                                             "and that you can log into the platform. If you are unsure how to proceed, "
                                             "please contact the Kortical team for assistance on slack "
                                             "(fastest response times) or email support@kortical.com")
            if throw and response.status_code not in [200, 201, 202, 204]:
                raise Exception(f"{function.__name__.upper()} Request [{url}] failed with status code [{response.status_code}]\n\n{response.content.decode()}")
            return response
        # Our nginx controller may have caused a config reload, this drops existing connections
        # and so we need to retry here in the case of a connection error
        except (requests.exceptions.ConnectionError, requests.exceptions.ReadTimeout) as e:
            if retry_index == num_retries:
                raise e
            print_error(f"Retrying due to connection drop")
            time.sleep(1)
        except ConnectionRefusedError as e:
            if retry_index == num_retries:
                raise e
            # backoff
            sleep = back_off_seconds ** retry_index
            print_error(f"Retrying after [{sleep}] seconds, as user has been logged out.")
            time.sleep(sleep)
            # login
            try:
                _login()
            except:
                pass

        retry_index += 1
        _reset_file_params(**kwargs)


def _reset_file_params(**kwargs):
    # Reset file params back to the start of their stream before we retry
    if 'files' in kwargs:
        # There are different ways of specifying files to pass to requests, so we iterate through the
        # potential options looking for streams that we can reset
        for file_tuple_or_stream in kwargs['files'].values():
            if isinstance(file_tuple_or_stream, IOBase):
                file_tuple_or_stream.seek(0)
            else:
                for param in file_tuple_or_stream:
                    if isinstance(param, IOBase):
                        param.seek(0)


def _set_url(url):
    global project_url
    global website_url

    # check and fix the url
    decomposed_url = urlparse(url)
    if len(decomposed_url.scheme) == 0:
        url = f'https://{url}'
        decomposed_url = urlparse(url)
    project_url = url
    if not project_url.endswith('/'):
        project_url += '/'

    # If this is running from within a pod on the cluster, it will be accessing a UI pod directly and will need
    # to specify the login endpoint
    website_url = f'{project_url}login' if IS_KUBERNETES_ENVIRONMENT else f'{decomposed_url.scheme}://{decomposed_url.netloc}'
    if not website_url.endswith('/'):
        website_url += '/'


def _login():
    global project_url
    global website_url
    global email
    global password

    form = {'email': email, 'password': password}
    retries = 3
    response = None
    if not IS_KUBERNETES_ENVIRONMENT:
        login_url = f"{_get_website_url()}login_api"
    else:
        login_url = f"{_get_project_url()}login_api"

    while not response:
        try:
            response = session.post(login_url, data=form, timeout=LOGIN_TIMEOUT)
            if response.status_code != 200:
                raise Exception(f"Request login failed with status code [{response.status_code}]\n\n{response.content.decode()}")
        # Our nginx controller may have caused a config reload, this drops existing connections
        # and so we need to retry here in the case of a connection error
        except requests.exceptions.ConnectionError as e:
            if retries <= 0:
                if "Failed to establish a new connection" in str(e):
                    raise KorticalKnownException("It looks like your internet is down. If you are confident this is not the case please contact Kortical.")
                raise
            print_error(f"Retrying due to connection drop")
            retries -= 1
            time.sleep(1)

    if not IS_KUBERNETES_ENVIRONMENT:
        # Admin accounts will hit the portal page when they login to the website above, so call .get on their project url to trigger a lookup
        # of their session id from the main website db, this is similar to what happens automatically for non admin users.
        session.get(_get_project_url(), timeout=LOGIN_TIMEOUT)

    # If a kortical user is using a production system, issue warnings.
    # TODO: Find a better interactive warning system for kortical email users on prod systems
    #       that doesn't stop/harm Github actions.
    # if is_kortical_user_on_prod_platform(email, project_url):
    #
    #     if session.cookies.get("kortical_beta") == 'always':
    #         print_warning("Using beta production system...")
    #     elif active_recently():
    #         print_warning("Using live production system...")
    #     else:
    #         response = input(format_warning(f"System URL: [{kortical_config.get('system_url')}]\n"
    #                                         f"You are targeting a live production system! Actions:\n"
    #                                         f"\tTo proceed - write [production].\n"
    #                                         f"\tto cancel - press [ENTER].\n"))
    #         if response == 'production':
    #             pass
    #         else:
    #             print_info("In order to target the beta system, follow these steps:\n"
    #                        "\t1. Go to the platform portal page. Find the project which matches the last part "
    #                        "of your config's system URL; click [edit] to check that a beta IP address exists.\n"
    #                        "\t2. Find the active user that matches the email set up in your config; "
    #                        "ensure that the [beta] field is set to [Yes].")
    #             raise KorticalKnownException("Action cancelled.")


def _user_prompt_and_complete_config(url, encrypted_credentials):

    # Assumes that there is no global/local config stored on the cwd path.

    if url is None or encrypted_credentials is None:
        if is_interactive() == 'false':
            # ... only raise if non-interactive and not a console test
            raise Exception("Missing URL or credentials; these cannot be prompted in non-interactive mode.\n"
                            "To set these, run [kortical config init --quiet], [kortical config set system_url <system_url>] "
                            "and [kortical config credentials from_string <credentials_string>].")

    # Prompt user for URL, update config if it doesn't currently contain a URL
    if url is None:
        url = kortical_config.user_prompt_url()
    if kortical_config.get('system_url') is None:
        kortical_config.set('system_url', url)

    # Prompt user for credentials
    if encrypted_credentials is None:
        encrypted_credentials = kortical_config.user_prompt_credentials(url)

        print_question(f"Save credentials? [y/N]")
        response = input()
        if response.lower()[0] == 'y':
            kortical_config.set('credentials', encrypted_credentials)

    return url, encrypted_credentials

