# SYSTEM IMPORTS 
import json, inspect


class Wrapper:

    def __init__(self, response):
        self.response      = response 
        self.response_type = type(response)


    def get_data(self) -> dict or list:
        return self.response


    def to_json(self, pretty_print: bool = False) -> json:
        return json.dumps(self.response, **{'indent': 2} if pretty_print else {})


class Response:

    def __init__(self):
        pass 


    def returns(self, response: dict):
        return Wrapper(response)