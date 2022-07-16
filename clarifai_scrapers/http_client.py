# SYSTEM IMPORTS
import requests, json


class HttpClient:
    
    def __init__(self, *args, **kwargs):
        pass


    def make_request(
        self, 
        method: str, 
        endpoint: str, 
        body: dict = None,
        additionalHeaders: dict = {}
        ):

        method = method.lower()
        args   = {'headers': {**additionalHeaders}}
        req    = getattr(requests, method)
        
        if method == 'post':
            args['headers'] = {
                **args['headers'], 
                'Content-Type': 'application/json'
            }

        if body: 
            args['data'] = json.dumps(body)
        
        r = req(endpoint, **args)

        return r