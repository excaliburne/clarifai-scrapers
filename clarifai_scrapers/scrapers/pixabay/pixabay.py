# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

# UTILS
from clarifai_scrapers.utils.decorators import timed, add_all_args_to_self, page_size_limitation_if_bytes_requested

# CONSTS
from .endpoints import SEARCH_IMAGES_URL


class Pixabay(ScraperBase):

    def __init__(
        self, 
        api_key: str, 
        also_return_bytes: bool = False
        ):
        super().__init__()

        self.api_key  = api_key

        self.query    = ''
        self.page     = 1
        self.per_page = 30

        self.also_return_bytes = also_return_bytes


    def _make_request(self):
        params = {
            'api_key': self.api_key,
            'query': self.query,
            'page_num': self.page,
            'per_page': self.per_page
        }

        url      = self._url_handler.build(SEARCH_IMAGES_URL, params)
        response = self._http_client.make_request('get', url).json()

        return response
    

    @staticmethod
    def _template_search(pixabay_image_object: dict):
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

    
    @add_all_args_to_self
    @timed
    @page_size_limitation_if_bytes_requested
    def search(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 30,
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

        pixabay_response = self._make_request()
        pixabay_results  = pixabay_response.get('hits', [])
        results          = [self._template_search(image) for image in pixabay_results]

        return self._response.returns(results)






