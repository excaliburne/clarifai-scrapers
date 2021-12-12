from clarifai_scrapers.response import Response
from clarifai_scrapers.utils.url_handler import UrlHandler
from clarifai_scrapers.http_client import HttpClient


class ScraperBase:

    def __init__(self):
        self._response = Response()
        self._url_handler = UrlHandler()
        self._http_client = HttpClient()