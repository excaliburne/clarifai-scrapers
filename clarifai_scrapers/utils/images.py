# SYSTEM IMPORTS
import requests, base64


def image_url_to_base64(url: str):
    """
    Convert image url to base64 string

    Args:
        url (string): Image url

    Returns:
        [type]: [description]
    """
    encoded = base64.b64encode(requests.get(url).content)

    return encoded.decode('ascii') 