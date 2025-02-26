class KorticalKnownException(Exception):
    pass


def check_for_known_platform_errors(response, error_codes=[422]):
    if response.status_code in [200, 204]:
        return

    if response.status_code in error_codes:
        raise KorticalKnownException(response.text)

    response.raise_for_status()
