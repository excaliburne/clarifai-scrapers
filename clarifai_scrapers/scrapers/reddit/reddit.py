# SYSTEM IMPORTS

# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

# UTILS
from clarifai_scrapers.utils.decorators import timed, paginate, add_all_args_to_self
from clarifai_scrapers.scrapers.reddit.decorators import reset_last_utc
from clarifai_scrapers.utils import csvs

# CONSTS
from clarifai_scrapers.scrapers.reddit.endpoints import SEARCH_SUBMISSIONS_IN_SUBREDDIT_URL


class Reddit(ScraperBase):
    """
    Entry point for Reddict scraping/search activities

    Args:
        ScraperBase (Class)
    """

    def __init__(self):
        super().__init__()

        self.submissions = RedditSubmissions()
    
    
class RedditSubmissions(ScraperBase):
    """
    Specifically takes care

    Args:
        ScraperBase (Class): Inherits from
    """

    def __init__(self):
        super().__init__()

        self.query = ''
        self.per_page  = 30
        self.page_num  = 1
        self.last_utc  = None

    
    def __call__(self):
        pass
    

    @staticmethod
    def _template_search(submission_object: dict) -> dict:
        template = {
            'id': submission_object.get('id'),
            'alt_description': submission_object.get('title'),
            'urls': {
                'full': submission_object.get('url'),
                'thumb': submission_object.get('url')
            }
        }

        return template
    


    @staticmethod
    def _template_scrape(submission_object: dict, **kwargs) -> list:
        template = {
            'input.id': '',
            'input.data.image.url': submission_object.get('url'),
        }

        return template


    @timed
    def _make_request(self, **kwargs) -> list:
        params = {
            'subreddit': self.query,
            'per_page': self.per_page,
            'other_params': '' if not self.last_utc else f'&before={self.last_utc}'
        }

        url           = self._url_handler.build(SEARCH_SUBMISSIONS_IN_SUBREDDIT_URL, params)
        response      = self._http_client.make_request('get', url).json()
        self.update_last_utc(response)

        return response


    def update_last_utc(self, response: dict) -> None:
        last_utc = None

        try:
            last_utc = response['data'][-1]['created_utc']
        except IndexError:
            last_utc = None
        
        self.last_utc = last_utc


    @add_all_args_to_self
    @timed
    @reset_last_utc
    def search(
        self, 
        query: str, 
        per_page: int, 
        page_num: int,
        **additional_data: dict
        ) -> dict:
        """
        Search for submmitted images/videos in given subreddit

        Args:
            query (str): Subreddit
            per_page (int)
            page_num (int)

        Returns:
            dict: Search response object
        """
        
        pushshift_response = self._make_request()['data']
        results            = [self._template_search(submission) for submission in pushshift_response]

        return self._response.search(results=results, additional_data=additional_data)
    

    @add_all_args_to_self
    @paginate(30)
    def scrape(
        self, 
        query: str, 
        limit: int = 100,
        output_file_path: str = None, 
        **additional_data
        ):
        """
        Scrape submissions given a subreddit

        Args:
            query (str): Subreddit
            limit (int, optional): Number of inputs you want to generate. Defaults to 100.
            output_file_path (str, optional): Output file path for creating .csv
            **additional_data (dict): Args returned by decorators

        Returns:
            (list)
        """
        
        self.per_page = 100 # MAX amount pushfit supports
        csv_headers  = ['input.data.image.url', 'input.id']
        scraped_data = []

        while len(scraped_data) < limit:
            pushshift_response = self._make_request()['data']

            # we break the process when the current data array + last request data is more than the limit
            if len(scraped_data) + len(pushshift_response) > limit:
                length_of_data_to_trim = limit - (len(scraped_data) + len(pushshift_response))
                formatted              = [self._template_scrape(data) for data in pushshift_response[:length_of_data_to_trim]]
                scraped_data.extend(formatted)
                break
            
            formatted = [self._template_scrape(data) for data in pushshift_response]
            scraped_data.extend(formatted)
        
        csvs.write(csv_headers, scraped_data, output_file_path)

        return scraped_data