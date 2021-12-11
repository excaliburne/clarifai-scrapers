# SYSTEM 
import requests

# UTILS
from .endpoints import PIXABAY__GET
from clarifai_scrapers.utils.url_handler import UrlHandler
from clarifai_scrapers.utils.decorators import timed

# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

class Pixabay(ScraperBase):

    def __init__(self, api_key: str):
        super().__init__()

        self.api_key = api_key

        self.query = ''
        self.page_num = 1
        self.per_page = 30


    def _make_request(self):
        params = {
            'api_key': self.api_key,
            'query': self.query,
            'page_num': self.page_num,
            'per_page': self.per_page
        }

        url = UrlHandler().build(PIXABAY__GET, params)
        req = requests.get(url)

        return req.json()
    

    def _template_search(self, pixabay_image_object: dict):
        template = {
            "id": pixabay_image_object.get('id'),
            "alt_description": pixabay_image_object.get('pageURL'),
            "urls": {
                "full": pixabay_image_object.get('largeImageURL'),
                "thumb": pixabay_image_object.get('previewURL')
            }
        }

        return template


    def scrape(self, query, page_num, per_page):
        pass
        # self.query = query
        # self.page_num = page_num
        # self.per_page = per_page

        # return self._make_request()


    @timed
    def search(
        self, 
        query: str, 
        page_num: int, 
        per_page: int,
        **additional_data: dict
        ):
        """
        Query images from Pixabay API

        Args:
            query (str):
            page_num (int): 
            per_page (int): 

        Returns:
            dict: { "total": 0, "results": [] }
        """
        for param in list(locals().items())[1:]:
            setattr(self, param[0], param[1])

        pixabay_response = self._make_request()
        pixabay_results = pixabay_response.get('hits', [])

        results = [self._template_search(image) for image in pixabay_results]

        return self._response.search(results, additional_data)






