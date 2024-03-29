"""
NOT WORKING ANYMORE. PLEASE DON'T USE ANYMORE UNTIL FIXED :(

"""

# PACKAGES
from igramscraper.instagram import Instagram

# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

# THIS SCRAPER
from .decorators import reset_last_id

# UTILS
from clarifai_scrapers.utils.decorators import add_all_args_to_self, timed


class InstagramScraper(ScraperBase):

    def __init__(
        self,
        user_data: dict = None
        ):
        """

        Args:
            user_data (dict, optional): Should look like... 
                {'username': '', 'password': ''}
        """
        super().__init__()
        
        self.last_id = None
        self.query = ''
        self.per_page = 30
        self.page = 1

        self.instagram = Instagram()

        if user_data:
            self.instagram.with_credentials(*user_data.values())
            self.instagram.login()     


    @staticmethod
    def _filter_metadata(media_dict: dict) -> dict:
        return {
            'type': media_dict['type'],
            'square_images': media_dict['square_images'],
            'likes_count': media_dict['likes_count'],
        }


    def _make_request(self):
        req  = self.instagram.get_medias_by_tag
        args = {'count': self.per_page}

        if self.last_id is not None:
            args['max_id'] = self.last_id
        
        return req(self.query, **args)


    def _template_search(self, media: dict) -> dict:
        media_to_dict = media.__dict__

        image_url         = media_to_dict['image_high_resolution_url']
        metadata          = self._filter_metadata(media_to_dict)
        image_id          = media_to_dict['identifier']
        image_thumb       = media_to_dict['square_images'][0]
        image_bytes       = image_url
        image_description = media_to_dict['caption']

        template = {
            'id': image_id,
            'alt_description': image_description,
            'urls': {
                'full': image_bytes,
                'thumb': image_thumb,
                'url': image_url
            },
            'metadata': metadata
        }
        
        return template


    @timed
    @reset_last_id
    @add_all_args_to_self
    def search_media_by_hashtag(
        self, 
        query: str, 
        page: int = 1, 
        per_page: int = 30
        ) -> dict:

        results      = self._make_request()
        response     = [self._template_search(media) for media in results]
        self.last_id = response[-1]['id']

        return self._response.returns(results)


    # def scrape(
    #     self,
    #     hashtag: str,
    #     count: int = 30,
    #     output_file: str = None
    #     ):

    #     results = []
    #     decount = count
    #     current_page = 1

    #     if count <= 30 and output_file == None:
    #         current_result = self.search_media_by_hashtag(hashtag=hashtag, page_num=1, per_page=count)['results']
    #         results.extend(convert_to_scrape_format(current_result))
    #     else:
    #         while decount != 0:
    #             if decount >= 30:
    #                 current_result = self.search_media_by_hashtag(hashtag=hashtag, page_num=current_page, per_page=30)['results']
    #                 decount -= 30
    #             else:
    #                 current_result = self.search_media_by_hashtag(hashtag=hashtag, page_num=current_page, per_page=decount)['results']
    #                 decount = 0

    #             current_page += 1
    #             results.extend(convert_to_scrape_format(current_result))

    #     if output_file == None:
    #         return results
    #     else:
    #         formatted_rows = []
    #         for row in results:
    #             row['not concepts'] = []
    #             formatted_rows.append(row)
    #         write_data_to_csv(formatted_rows, output_file)
