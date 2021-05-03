# SYSTEM IMPORTS
import requests, base64


def get_as_base64(url):
    encoded = base64.b64encode(requests.get(url).content)
    return encoded.decode('ascii') 