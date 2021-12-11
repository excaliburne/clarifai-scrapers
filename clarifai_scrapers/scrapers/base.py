from clarifai_scrapers.response import Response


class ScraperBase:

    def __init__(self):
        self._response = Response()