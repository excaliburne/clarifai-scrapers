# SYSTEM IMPORTS
from __future__ import absolute_import, division, print_function

import argparse
import json
import time
import requests
import pandas as pd


PUSHSHIFT_META = 'https://api.pushshift.io/meta'
RATE_LIMIT_PER_MINUTE = requests.request(
    'GET',
    PUSHSHIFT_META
).json()['server_ratelimit_per_minute']
RATE_LIMIT = 1 / (RATE_LIMIT_PER_MINUTE / 60)


class Reddit:
    pushshift_meta = 'https://api.pushshift.io/meta'

    def __init__(self):
        self.last_utc = None
        self.current_page = 1
    
    def run_scraper(self, subreddit, output_file, per_page=100):
        all_data = []
        prev_last_utc = 'placeholder'

        pushshift_url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={per_page}'

        # get first page of results
        data, cur_last_utc = self.get_images(pushshift_url)
        all_data.extend(data)

        print(
            'Note: If you need to stop the script, hit `ctrl + c` once, which will write out any results and safely exit.'
        )
        print('total collected items: {}'.format(len(all_data)))

        # begin while loop, using the cur_last_id to paginate through results
        while prev_last_utc != cur_last_utc:
            try:
                # trying to respect PushShift's api limit
                time.sleep(RATE_LIMIT)

                # set cur_last_id as new prev_last_id
                prev_last_utc = cur_last_utc

                # build new pushshift url and get images
                pushshift_url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={per_page}&before={prev_last_utc}'
                data, cur_last_utc = self.get_images(pushshift_url)
                all_data.extend(data)

                print('total collected items: {}'.format(len(all_data)))

                if cur_last_utc == None:
                    break

            # adding this so it safely quits if there's a massive subreddit and you don't want to grab all of it.
            except KeyboardInterrupt:
                print("Manual keyboard interrupt detected. Attempting to save current results and exit.")
                break

        df = pd.DataFrame(all_data)
        df.to_csv(self.output_file, index=False)
        print(f'Results saved to output file: {output_file}')

    
    def get_images(self, pushshift_url, sparse_meta=False):
        data = []
        last_utc = None

        res = requests.request('GET', pushshift_url)
        res_data = res.json()['data']

        for item in res_data:
            item_utc = item['created_utc']
            item_url = item['url']

            # various domain/url templates which hosts the direct image
            im_domains = ['https://i.redd.it', 'https://i.imgur.com']

            if len([item_url for x in im_domains if x in item_url]) > 0:
                if not sparse_meta:
                    metadata_keys = list(item.keys())
                    metadata_keys.remove('url')
                else:
                    metadata_keys = ['subreddit', 'permalink', 'author']

                metadata_dict = {key: item[key] for key in metadata_keys}

                temp_dict = {}
                temp_dict['url'] = item_url
                temp_dict['metadata'] = json.dumps(metadata_dict)

                data.append(temp_dict)
                
            last_utc = item_utc

        return data, last_utc
    

    def search_images(self, subreddit, per_page, page):
        pushshift_url = f'https://api.pushshift.io/reddit/search/submission/?subreddit={subreddit}&size={per_page}'

        if page == 1:
            self.last_utc = None

        if self.last_utc:
            pushshift_url = pushshift_url + f'&before={self.last_utc}'

        data, cur_last_utc = self.get_images(pushshift_url)
        self.last_utc = cur_last_utc

        returned_dict = {
            'total': 0,
            'results': []
        }

        for item in data:
            metadata_to_dict = json.loads(item['metadata'])
            image_id = metadata_to_dict['id']
            image_thumb = metadata_to_dict['thumbnail']
            image_description = metadata_to_dict['title']

            template = {
                'id': image_id,
				'alt_description': image_description,
				'urls': {
					'full': item['url'],
					'thumb': item['url']
				}
            }

            returned_dict['results'].append(template)
            returned_dict['total'] = returned_dict['total'] + 1

        return returned_dict

