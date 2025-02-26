from kortical.cloud import _random_seed
from kortical.config import kortical_config
from kortical.helpers.encryption_helpers import decrypt


def get_user_email():
    encrypted_credentials = kortical_config.get('credentials')
    credentials = decrypt(encrypted_credentials, key=_random_seed)
    email = credentials['email']
    return email