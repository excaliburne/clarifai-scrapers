# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

# UTILS
from clarifai_scrapers.utils.decorators import page_size_limitation_if_bytes_requested

# CONSTS
from .endpoints import SEARCH_PHOTOS


class Flickr(ScraperBase):
    def __init__(
        self, 
        api_key: str,
        also_return_bytes: bool = False
        ):
        super().__init__()

        self.api_key = api_key

        self.also_return_bytes = also_return_bytes


    def _make_request(
        self,
        endpoint: str,
        method: str,
        path_variables: dict = {},
        query_params: dict = {},
        body: dict = {}
        ):

        url      = self._url_handler.build(endpoint, path_variables, query_params)
        response = self._http_client.make_request(
            method, 
            url,
            body,
        )

        return response


    @staticmethod
    def _to_response_schema(flickr_image_object):
        response_schema = {
            'id': flickr_image_object.get('id'),
            'alt_description': flickr_image_object.get('title'),
            'urls': {
                'full': flickr_image_object.get('url_l_cdn'),
                'thumb': flickr_image_object.get('url_m_cdn') or flickr_image_object.get('url_c_cdn') \
                    or flickr_image_object.get('url_l_cdn')
            }
        }

        return response_schema
    

    @page_size_limitation_if_bytes_requested
    def search(
        self,
        query: str,
        page: int = 1,
        per_page: int = 30,
        sort: str = 'relevance'
    ):  
        """
        Search for images by query

        Args:
            query (str)
            page (int, optional): Defaults to 1.
            per_page (int, optional): Defaults to 30.
            sort (str, optional): Defaults to 'relevance'.
                - Possible values are: date-posted-asc, date-posted-desc, date-taken-asc, 
                                       date-taken-desc, interestingness-desc, interestingness-asc, 
                                       relevance

        Returns:
            (str<json> or list<dict>)
        """
        response = self._make_request(
            SEARCH_PHOTOS,
            method="GET",
            path_variables={
                'query': query,
                'page': page,
                'per_page': per_page,
                'api_key': self.api_key,
                'sort': sort
            }
        )

        response_schema = [self._to_response_schema(image_object) for image_object in response.json()['photos']['photo']] \
            if response.status_code == 200 else []

        return self._response.returns(response_schema)