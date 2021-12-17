# SYSTEM IMPORTS
import requests, base64


def get_as_base64(url):
    """
    Convert image url to base64 string

    Args:
        url (string): Image url

    Returns:
        [type]: [description]
    """
    encoded = base64.b64encode(requests.get(url).content)
    return encoded.decode('ascii') 