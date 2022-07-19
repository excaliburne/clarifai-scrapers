# SYSTEM IMPORTS 
import json, inspect

# UTILS
from clarifai_scrapers.utils.images import image_url_to_base64


class Wrapper:

    def __init__(self, response):
        self.response      = response 
        self.response_type = type(response)


    def get_data(self) -> dict or list:
        return self.response


    def to_json(self, pretty_print: bool = False) -> json:
        return json.dumps(self.response, **{'indent': 2} if pretty_print else {})


class Response:

    def __init__(
        self,
        also_return_bytes: bool = False
        ):

        self.also_return_bytes = also_return_bytes


    def returns(self, response: dict or list) -> Wrapper:

        if self.also_return_bytes:
            for image_object in response:
                if image_object['urls']['full'] is not None:
                    image_object['bytes'] = {
                        'full': image_url_to_base64(image_object['urls']['full']),
                        'thumb': image_url_to_base64(image_object['urls']['thumb'])
                    }

        return Wrapper(response)