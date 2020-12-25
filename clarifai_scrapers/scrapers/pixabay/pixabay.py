import requests
import urllib

from .endpoints import SEARCH_PHOTO


class Pixabay:
    def __init__(self, api_key):
        self.api_key = api_key
        self.query = ''
        self.page_num = 1
        self.per_page = 30

        self.json_response_template = {
            "total": 0,
            "results": []
        }

    def make_request(self):
        req = requests.get(SEARCH_PHOTO(self.api_key, self.query, self.page_num, self.per_page)).json()
        return req
    
    def scrape(self, query, page_num, per_page):
        self.query = query
        self.page_num = page_num
        self.per_page = per_page

        return self.make_request()

    def scrape_toolbox_format(self, query, page_num, per_page):
        self.query = query
        self.page_num = page_num
        self.per_page = per_page

        response = self.make_request()
        results = response.get('hits')
        total = 0

        for idx, image in enumerate(results):
            if idx < self.per_page:
                total += 1
                img_id = image.get('id')
                img_thumb = image.get('previewURL')
                img_full = image.get('largeImageURL')
                alt_description = image.get('pageURL')

                results_dict = {
                    "id": img_id,
                    "alt_description": alt_description,
                    "urls": {
                        "full": img_full,
                        "thumb": img_thumb
                    }
                }

                self.json_response_template['results'].append(results_dict)
                self.json_response_template.update({ 'total': total })
            
        return self.json_response_template






