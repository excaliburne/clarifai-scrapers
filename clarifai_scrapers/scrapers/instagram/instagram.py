# PACKAGES
from igramscraper.instagram import Instagram

# UTILS
from clarifai_scrapers.utils.instagram import convert_to_scrape_format
from clarifai_scrapers.utils.write import write_data_to_csv
from clarifai_scrapers.utils import images

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


    def search_media_by_hashtag(
        self, 
        hashtag, 
        page_num, 
        per_page
        ):

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
            image_thumb = images.get_as_base64(media_to_dict['square_images'][0])
            image_url = images.get_as_base64(media_to_dict['image_high_resolution_url'])
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


    def scrape(
        self,
        hashtag: str,
        count: int = 30,
        output_file: str = None
        ):

        results = []
        decount = count
        current_page = 1

        if count <= 30 and output_file == None:
            current_result = self.search_media_by_hashtag(hashtag=hashtag, page_num=1, per_page=count)['results']
            results.extend(convert_to_scrape_format(current_result))
        else:
            while decount != 0:
                if decount >= 30:
                    current_result = self.search_media_by_hashtag(hashtag=hashtag, page_num=current_page, per_page=30)['results']
                    decount -= 30
                else:
                    current_result = self.search_media_by_hashtag(hashtag=hashtag, page_num=current_page, per_page=decount)['results']
                    decount = 0

                current_page += 1
                results.extend(convert_to_scrape_format(current_result))

        if output_file == None:
            return results
        else:
            formatted_rows = []
            for row in results:
                row['not concepts'] = []
                formatted_rows.append(row)
            write_data_to_csv(formatted_rows, output_file)
