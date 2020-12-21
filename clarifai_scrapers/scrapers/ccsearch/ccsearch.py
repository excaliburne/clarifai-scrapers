'''
Scraper for https://ccsearch.creativecommons.org/. Given a series of search queries,
returns a csv of urls. Filtered by commercially-usable Creative Commons licenses by default.

Example usage:
python ccsearch_scraper.py --query balloon,fish,"potato chip" --output_name ~/Downloads/ccsearch_test.csv

Note regarding --license_type and --specific_licenses flags: the search will always default to the more restrictive option.
'''
from __future__ import absolute_import, division, print_function

import argparse
import json
import time

import numpy as np
import pandas as pd
import requests
from tqdm import tqdm


class CCsearch:
	def __init__(self, license_type: str, 
					   per_page: int, 
					   search_limit: int, 
					   return_raw_data: bool,
					   specific_licenses='cc0,pdm,by,by-sa'):
		self.license_type = license_type
		self.per_page = per_page
		self.search_limit = search_limit
		self.return_raw_data = return_raw_data
		self.specific_licenses = specific_licenses

	
	def run(self, keywords, output_name, return_formatted_dict):
		all_data = []

		queries = keywords.split(',')

		for query in tqdm(queries, desc='queries'):
			search_results = self.run_ccsearch(query, self.license_type, self.per_page, self.search_limit)
			all_data.extend(search_results)

		if self.return_raw_data == True:
			df = pd.DataFrame(all_data)
		elif return_formatted_dict == True:
			json_data = self.return_formatted_dict(all_data)
			return json_data
		else:
			df = self.parse_ccsearch_into_upload_csv(all_data)

		df.to_csv(output_name, index=False)
		print(f'Output csv saved to: {output_name}')
		print(
				"** Note: When uploading these to an app, do so at a slower rate than normal. They seem to timeout often."
		)

	def run_ccsearch(self, query, license_type, per_page, search_limit):
		'''
		Input:
			• query 				> search query
			• license_type	> options are "commercial", "modification", "commercial,modification", or "all"
			• per_page			> number of results to return per search. limit 1 - 500
			• search_limit	> default and max 10000. can lower if you want less results.
		Output:
			• list of dicts of search results
		'''
		base_url = 'http://api.creativecommons.engineering/v1/images/?'

		probe_search_url = f'{base_url}q={query}&license_type={license_type}&page_size=1'
		probe_search_res = requests.request("GET", probe_search_url)
		result_count = probe_search_res.json()['result_count']

		if search_limit < result_count:
			result_count = search_limit

		if result_count < per_page:
			per_page = result_count

		search_results = []

		error_count = 0

		for page_num in tqdm(range(0, int(np.ceil(result_count / per_page))), desc=f'results for {query}'):
			search_url = f'{base_url}q={query}&license_type={license_type}&page_size={per_page}&page={page_num}'
			search_res = requests.request("GET", search_url)

			if search_res.status_code == 200:
				results = search_res.json()['results']
				_ = [x.update({'search_query': query}) for x in results]
				search_results.extend(results)
			else:
				if error_count < 3:
					error_count += 1
					time.sleep(1)
					continue
				else:
					print(f"There's been frequent errors with this search. Stopping with current query [{query}].")
					return search_results

		# below used to filter out duplicate entries
		search_results = list({v['id']: v for v in search_results}.values())

		return search_results


	def parse_ccsearch_into_upload_csv(self, search_results):
		'''
		Input:
			• "search_results"	> the list of jsons from run_ccsearch
			• "query" 					> the original query term for the above
		Output:
			a pandas dataframe with ["url", "metadata"]
				• "url"				> the direct image url
				• "metadata"	> any additional info about the result from the ccsearch, usually:
					• creator, creator_url, id, license, license_version, source, title, search_query
		'''

		print(json.dumps(search_results, indent=2))
		df_orig = pd.DataFrame(search_results)

		# keep some of the columns as metadata
		columns = [
				'creator', 'creator_url', 'id', 'license', 'license_version', 'source', 'title',
				'search_query'
		]
		df_orig['metadata'] = df_orig[columns].to_dict(orient='records')

		for i, each in df_orig.iterrows():
			df_orig['metadata'].iat[i] = json.dumps(each['metadata'])

		df_new = df_orig[['url', 'metadata']]

		return df_new


	def return_formatted_dict(self, search_results):
		json_data = {
			"total": 0,
			"results": []
		}
		
		total = 0

		for result in search_results:
			total += 1
			id = result.get('id')
			alt = result.get('title')
			url = result.get('url')
			thumb = result.get('thumbnail')

			temp_dict = {
				"id": id,
				"alt_description": alt,
				"urls": {
					"full": url,
					"thumb": thumb
				}
			}
			json_data['results'].append(temp_dict)

		json_data.update({'total': total})
		
		return json_data
			
