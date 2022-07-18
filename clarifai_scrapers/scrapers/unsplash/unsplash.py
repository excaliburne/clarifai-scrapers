# MODULES
from clarifai_scrapers import response
from clarifai_scrapers.scrapers.base import ScraperBase

# 
from clarifai_scrapers.response import Response

# CONSTS
from .endpoints import LIST_PHOTOS, SEARCH_PHOTOS


class Unsplash(ScraperBase):
    def __init__(self, api_key: str):
        super().__init__()

        self.api_key  = api_key
        

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
            additionalHeaders={
                'Authorization': f'Client-ID {self.api_key}'
            }
        )

        return response
    

    def _to_response_schema(self, unsplash_image_object):
        response_schema = {
            'id': unsplash_image_object.get('id'),
            'alt_description': unsplash_image_object.get('alt_description'),
            'urls': {
                'full': unsplash_image_object['urls']['full'],
                'thumb': unsplash_image_object['urls']['thumb']
            }
        }

        return response_schema


    def list_photos(
        self,
        page: int = None,
        per_page: int = None,
        order_by: str = None
    ):
        """
        List Photos

        Args:
            page (int, optional)
            per_page (int, optional)
            order_by (str, optional): Can be...
                - latest (default)
                - oldest  
                - popular

        Returns:
            (str<json> or list<dict>)
        """
        response = self._make_request(
            LIST_PHOTOS, 
            method="GET",
            query_params={
                'page': page,
                'per_page': per_page,
                'order_by': order_by
            }
        )

        response_schema = [self._to_response_schema(image_object) for image_object in response.json()] \
            if response.status_code == 200 else []

        return Response().returns(response_schema)
    

    def search_photos(
        self,
        query: str,
        page: int = None,
        per_page: int = None,
        order_by: str = None,
        content_filter: str = None,
        color: str = None,
        orientation: str = None
    ) -> str or dict:
        """
        Search Photos

        Args:
            query (str)
            page (int, optional): Unsplash API default to 1
            per_page (int, optional): Unsplash API default to 10
            order_by (str, optional): Valid values:
                - latest
                - relevant
            content_filter (str, optional): Limit results by content safety. Valid values:
                - low
                - high
            color (str, optional): Filter results by color. Valid values: 
                - black_and_white
                - black
                - white
                - yellow
                - orange 
                - red
                - purple 
                - magenta,
                - green
                - teal
                - blue
            orientation (str, optional): Filter by photo orientation. Valid values: 
                - landscape
                - portrait 
                - squarish

        Returns:
            (str<json> or list<dict>)
        """

        response = self._make_request(
            SEARCH_PHOTOS, 
            method="GET",
            query_params={
                'query': query,
                'page': page,
                'per_page': per_page,
                'order_by': order_by,
                'content_filter': content_filter,
                'color': color,
                'orientation': orientation
            }
        )

        to_response_schema = [self._to_response_schema(image_object) for image_object in response.json()['results']] \
            if response.status_code == 200 else []

        return self._response.returns(to_response_schema)