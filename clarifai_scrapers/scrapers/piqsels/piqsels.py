# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

# PACKAGES
from bs4 import BeautifulSoup

# UTILS
from clarifai_scrapers.utils.decorators import add_all_args_to_self, timed

# CONSTS
from .endpoints import SEARCH_URL


class Piqsels(ScraperBase):

    def __init__(self):
        super().__init__()


    def _make_request(self) -> 'bs4.BeautifulSoup':
        """
        Makes request to Piqsels API 

        Returns:
            (bs4.BeautifulSoup)
        """
        params = {
            'query': self.query,
            'page_num': self.page_num
        }

        url      = self._url_handler.build(SEARCH_URL, params)
        response = self._http_client.make_request('get', url)
        soup     = BeautifulSoup(response.content, 'html.parser')

        return soup
    

    def _get_image_grid(self) -> 'bs4.element.ResultSet':
        """
        Returns the html image grid page

        Returns:
            (bs4.element.ResultSet)
        """
        soup        = self._make_request()
        results     = soup.find(id='flow')
        li_elements = results.find_all('li')

        return li_elements


    @staticmethod
    def _template_search(list_element: dict) -> dict:
        """
        Returns template that parsed list_elements to the template dictionnary

        Args:
            list_element (dict)

        Returns:
            dict: Template
        """
        a_tag     = list_element.find('a')
        href_link = a_tag['href']
        img       = list_element.find('img')
        thumb_img = img['data-src']
        full_img  = img['data-srcset'].split(' ')[1].split(',')[1]
        img_id    = href_link[-5:]
        
        template = {
            'id': img_id,
            'alt_description': href_link,
            'urls': {
                'full': full_img,
                'thumb': thumb_img
            }
        }

        return template


    # TODO: Need to find a better workaround for the pagination
    @add_all_args_to_self
    @timed
    def search(
        self, 
        query: str, 
        page_num: int,
        per_page: int,
        **additional_data
        ):
        """
        Search images

        Args:
            query (str)
            page_num (int)
            per_page (int)

        Returns:
            (dict): Response dict
        """

        list_elements = self._get_image_grid()
        results       = [self._template_search(list_element) for list_element in list_elements[:per_page]]
            
        return self._response.search(results=results, additional_data=additional_data)











