# SYSTEM IMPORTS 
import json, inspect


class Wrapper:
    def __init__(self, response):

        self.response      = response 
        self.response_type = type(response)
    

    def __call__(self):
        return self.response
        

    def __getattribute__(self, attribute_name):
        return super().__getattribute__(attribute_name)


    def get_response(self):
        return self.response


    def to_json(self, pretty_print: bool = False):

        return json.dumps(self.response, **{'indent': 2} if pretty_print else {})


class Response:
  
    def returns(self, response: dict):

        return Wrapper(response)()