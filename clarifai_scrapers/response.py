# SYSTEM IMPORTS 
import json, inspect


class Wrapper:
    def __init__(self, response):

        self.response      = response 
        self.response_type = type(response)
    

    def __call__(self):
        stack             = inspect.stack()
        get_method_called = str(stack[3].code_context).split(' ')[-1].split('.')[-1].split('()')[0]

        if 'to_json' in get_method_called:
            return self
        else:
            return self.response


    def to_json(self, pretty_print: bool = False):

        return json.dumps(self.response, **{'indent': 2} if pretty_print else {})

class Response:
  
    def returns(self, response: dict):

        return Wrapper(response)()