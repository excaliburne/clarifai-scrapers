# SYSTEM IMPORTS
import requests, json


class HttpClient:
    
    def __init__(self, *args, **kwargs):
        pass


    def make_request(self, method, endpoint, body=None):
        args = {}
        req = getattr(requests, method)

        # args['headers'] = {'Authorization': f'Key {self.token}'}
        
        if method == 'post':
            args['headers'] = {**args['headers'], 'Content-Type': 'application/json'}

        if body: 
            args['data'] = json.dumps(body)
        
        r = req(endpoint, **args)

        return r.json()