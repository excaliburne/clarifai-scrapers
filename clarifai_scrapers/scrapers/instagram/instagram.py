from igramscraper.instagram import Instagram

instagram = Instagram()

class InstagramScraper:
    def __init__(self):
        self.last_id = None
            
    def _filter_metadata(self, media_dict: dict):
        return {
            'type': media_dict['type'],
            'square_images': media_dict['square_images'],
            'likes_count': media_dict['likes_count'],
        }


    def search_media_by_hashtag(self, hashtag, page_num, per_page):
        if page_num == 1:
            self.last_id = None

        if self.last_id == None: 
            medias = instagram.get_medias_by_tag(hashtag, count=per_page)
        else:
            medias = instagram.get_medias_by_tag(hashtag, count=per_page, max_id=self.last_id)

        returned_dict = {
            'total': 0,
            'results': []
        }

        for media in medias:
            media_to_dict = media.__dict__

            metadata = self._filter_metadata(media_to_dict)
            image_id = media_to_dict['identifier']
            image_thumb = media_to_dict['square_images'][0]
            image_url = media_to_dict['image_high_resolution_url']
            image_description = media_to_dict['caption']

            template = {
                'id': image_id,
				'alt_description': image_description,
				'urls': {
					'full': image_url,
					'thumb': image_thumb
				},
                'metadata': metadata
            }

            returned_dict['results'].append(template)
            returned_dict['total'] = returned_dict['total'] + 1

        self.last_id = returned_dict['results'][-1]['id']
        return returned_dict


    def scrape(self):
        pass