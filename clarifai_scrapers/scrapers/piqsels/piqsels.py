import requests
import json

from bs4 import BeautifulSoup

from .endpoints import SEARCH

class PiqselsScraper:
    def __init__(self):
        self.total = 0
        self.json_response_template = {
            "total": 0,
            "results": []
        }
        self.page_num = 1
        self.query = ''

    def _start_bs4_machine(self):
        page = requests.get(SEARCH(self.query, page_num=self.page_num))
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup
    
    def _get_image_grid(self):
        soup = self._start_bs4_machine()
        results = soup.find(id='flow')
        li_elements = results.find_all('li')
        return li_elements
        
    def scrape(self, query, page_num, per_page):
        self.page_num = page_num
        self.query = query

        li_elements = self._get_image_grid()

        for idx, li in enumerate(li_elements):
            print(idx)
            if idx < per_page:
                self.total += 1
                a_tag = li.find('a')
                href_link = a_tag['href']
                img = li.find('img')
                thumb_img = img['data-src']
                full_img = img['data-srcset'].split(' ')[1].split(',')[1]
                img_id = href_link[-5:]

                results_dict = {
                    "id": img_id,
                    "alt_description": href_link,
                    "urls": {
                        "full": full_img,
                        "thumb": thumb_img
                    }
                }

                self.json_response_template.update({'total': self.total})
                self.json_response_template['results'].append(results_dict)
            
        return self.json_response_template











