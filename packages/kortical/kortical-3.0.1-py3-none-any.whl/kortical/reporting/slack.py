import logging
from slack_sdk import WebClient
import time

from kortical.helpers.exceptions import KorticalKnownException
from kortical.logging import logging_config

logging_config.init_logger()
logger = logging.getLogger(__name__)

kortical_slack_bot_token = None
kortical_notify_slack = True
kortical_slack_test_channel = None
web_client = None

SLACK_CHAR_LIMIT = 3000


def _get_text_block(text):
    block = {
               'type': 'section',
               'text': {
                   'type': 'mrkdwn',
                   'text': text
               }
           }
    return block


def _get_text_chunks(text):
    codify = False
    if text.startswith('```') and text.endswith('```'):
        codify = True
        text = text.lstrip('```').rstrip('```')

    start = 0
    while start < len(text):
        end = start + (SLACK_CHAR_LIMIT - 10)
        text_chunk = f'```{text[start:end]}```' if codify else f'{text[start:end]}'
        yield text_chunk
        start = end

def _check_slack_response(response):
    if not response.get('ok', False):
        message = f'Slack API call failed with error [{response.get("error")}] ' \
                  f'and detail [{response.get("response_metadata")}]'
        logger.error(message)
        logger.debug(f'Full Slack response: {response}')
        raise Exception(message)


def init(slack_bot_token, notify_slack=True, slack_test_channel=None):
    global kortical_slack_bot_token
    global kortical_notify_slack
    global kortical_slack_test_channel
    global web_client

    kortical_slack_bot_token = slack_bot_token
    kortical_notify_slack = notify_slack
    kortical_slack_test_channel = slack_test_channel
    web_client = WebClient(kortical_slack_bot_token)


def post_message_to_slack(channels, **kwargs):
    global kortical_notify_slack
    global web_client

    if web_client is None:
        raise KorticalKnownException("You must first run kortical.reporting.slack.init() with a slack bot token.")

    if isinstance(channels, str):
        channels = [channels]

    if kortical_notify_slack is True:
        channels_to_notify = channels
    elif kortical_slack_test_channel is not None:
        channels_to_notify = [kortical_slack_test_channel]
    else:
        channels_to_notify = []

    logger.info(f"kortical: posting message to slack channels {channels_to_notify}")
    for channel in channels_to_notify:
        response = web_client.chat_postMessage(channel=channel, **kwargs)
        _check_slack_response(response)


def post_simple_message_to_slack(channels, title, message):
    global kortical_notify_slack
    global web_client

    if web_client is None:
        raise KorticalKnownException("You must first run kortical.reporting.slack.init() with a slack bot token.")

    # Short message
    if len(message) < SLACK_CHAR_LIMIT:
        post_message_to_slack(channels, blocks=[_get_text_block(title),
                                                {'type': 'divider'},
                                                _get_text_block(message),
                                                {'type': 'divider'}])

    # Long message (needs to be chunked)
    else:
        post_message_to_slack(channels, blocks=[_get_text_block(title),
                                                {'type': 'divider'}])

        for chunk in _get_text_chunks(message):
            block = _get_text_block(chunk)
            post_message_to_slack(channels, blocks=[block])
            time.sleep(1)

        post_message_to_slack(channels, blocks=[{'type': 'divider'}])
