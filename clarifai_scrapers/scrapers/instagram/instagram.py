import json
import yaml

import os 

from instascrape import InstaScrape

class InstagramScaper:
    def __init__(self):
        self.instagram = InstaScrape()
        self.this_dir = os.path.dirname(os.path.realpath(__file__))
        self.yml_path = self.this_dir + '/page_index.yml'
        self.json_response = {
            "total": 0,
            "results": []
        }
        self.urls_arr = []


    def get_post_from_tag(self, tag):
        res = self.instagram.scrape_hashtag(tag)
        return res



    #### igramscaper package implementation
    # def _open_page_index(self):
    #     with open(self.yml_path) as file:
    #         page_index_content = yaml.load(file, Loader=yaml.FullLoader)
    #         return page_index_content
    
    # def _get_current_page_index(self):
    #     current_page_index = self._open_page_index()['current_page']
    #     return current_page_index

    # def _get_last_id(self):
    #     current_media_id = self._open_page_index()['current_id']
    #     return current_media_id
    
    # def _write_current_page_index(self, page_num, lowest_id):
    #     write_dict = {
    #         'current_page': page_num,
    #         'current_id': lowest_id
    #     }
    #     with open(self.yml_path, 'w') as file:
    #         documents = yaml.dump(write_dict, file)

    # def test(self):
    #     medias = self

    # def search_by_tag(self, tag, count, page_num=1):
    #     # if page_num >= 2:
    #     #     last_id = self._get_last_id()
    #     #     print(f"page num is {page_num}, last_id is: ", last_id)
    #     #     medias = self.instagram.get_medias_by_tag(tag, count=count, max_id=last_id)
    #     # elif page_num == 1:
    #     #     print("page num is 1")
    #     #     medias = self.instagram.get_medias_by_tag(tag, count=count)

    #     medias = self.instagram.get_medias_by_tag(tag, count=count)
        
    #     total = 0
    #     lowest_media_id = 0

    #     for idx, media in enumerate(medias):
    #         total += 1
    #         if idx == count-1:
    #             lowest_media_id = int(media.identifier)

    #         self.json_response['results'].append({
    #             "id": media.identifier,
    #             "alt_description": media.caption,
    #             "urls": {
    #                 "full": media.image_high_resolution_url,
    #                 "thumb": media.thumbnail_src
    #             }
    #         })
        
    #     self._write_current_page_index(page_num, lowest_media_id)
    #     self.json_response['total'] = total
        
    #     return self.json_response