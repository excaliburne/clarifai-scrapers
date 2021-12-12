# SYSTEM IMPORTS
from __future__ import absolute_import, division, print_function

import argparse
import json
import time
import requests
import pandas as pd

# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

# UTILS
from clarifai_scrapers.utils.decorators import timed
from clarifai_scrapers.scrapers.reddit.decorators import reset_last_utc

# CONSTS
from clarifai_scrapers.scrapers.reddit.endpoints import SEARCH_SUBMISSIONS_IN_SUBREDDIT


class Reddit(ScraperBase):

    def __init__(self):
        super().__init__()

        # self.last_utc = None
        # self.current_page = 1
        # self.all_data = []

        self.submissions = RedditSubmissions(self)
    

    def run_scraper(
        self, 
        subreddit: str, 
        output_file: str = None, 
        per_page: int = 100, 
        limit: int = 100
        ):
        pass
        # # if limit is under 100 we only want to page argument as limit
        # if limit <= 100:
        #     per_page = limit

        # # base pushfit url
        # pushshift_url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={per_page}'

        # # get first page of results and join the new data to existing if any
        # data, cur_last_utc = self.get_images(pushshift_url)
        # self.all_data.extend(data)

        # print('total collected items: {}'.format(len(self.all_data)))

        # # begin while loop, using the cur_last_id to paginate through results
        # while self.last_utc != cur_last_utc and len(self.all_data) < limit:
        #     try:
        #         # trying to respect PushShift's api limit
        #         time.sleep(RATE_LIMIT)

        #         # set cur_last_id as new prev_last_id
        #         self.last_utc = cur_last_utc

        #         # build new pushshift url and get images
        #         pushshift_url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={per_page}&before={self.last_utc}'
        #         data, cur_last_utc = self.get_images(pushshift_url)
        #         self.all_data.extend(data)

        #         print('total collected items: {}'.format(len(self.all_data)))

        #         if cur_last_utc == None:
        #             break

        #     # adding this so it safely quits if there's a massive subreddit and you don't want to grab all of it.
        #     except KeyboardInterrupt:
        #         print("Manual keyboard interrupt detected. Attempting to save current results and exit.")
        #         break
        
        # self.all_data = self.all_data[:limit]
        # filtered_data = filter_metadata(self.all_data)

        # if output_file == None:
        #     filtered_data = format_concepts(filtered_data)
        #     return filtered_data
        # else:
        #     write_data_to_csv(filtered_data, output_file)

    
class RedditSubmissions:

    def __init__(self, parent):

        for key, value in parent.__dict__.items():
            setattr(self, key, value)

        self.subreddit = ''
        self.per_page = 30
        self.page_num = 1
        self.last_utc = None

    
    def __call__(self):
        pass


    @staticmethod
    def _template(submission_object):
        template = {
            'id': submission_object.get('id'),
            'alt_description': submission_object.get('title'),
            'urls': {
                'full': submission_object.get('url'),
                'thumb': submission_object.get('url')
            }
        }

        return template


    def _make_request(self):
        params = {
            'subreddit': self.subreddit,
            'page_num': self.page_num,
            'per_page': self.per_page,
            'other_params': '' if not self.last_utc else f'&before={self.last_utc}'
        }

        url = self._url_handler.build(SEARCH_SUBMISSIONS_IN_SUBREDDIT, params)
        response = self._http_client.make_request('get', url)

        return response


    @timed
    @reset_last_utc
    def search(
        self, 
        subreddit: str, 
        per_page: int, 
        page_num: int,
        **additional_data: dict
        ) -> dict:

        for param in list(locals().items())[1:]:
            setattr(self, param[0], param[1])
        
        unshift_response = self._make_request()['data']

        self.last_utc = unshift_response[-1]['created_utc']

        results = [self._template(submission) for submission in unshift_response]

        return self._response.search(results, additional_data)