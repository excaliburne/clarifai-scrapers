# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

# UTILS
from clarifai_scrapers.utils.decorators import add_all_args_to_self, timed

# CONSTS
from .endpoints import SEARCH_IMAGES_URL



class CCsearch(ScraperBase):

	def __init__(self):
		super().__init__()

		self.license_type = 'all'


	def _make_request(self) -> dict: 
		params = {
            'query': self.query,
            'page_num': self.page_num,
			'per_page': self.per_page,
			'license_type': self.license_type
        }

		url      = self._url_handler.build(SEARCH_IMAGES_URL, params)
		response = self._http_client.make_request('get', url).json()
		
		return response


	@staticmethod
	def _template_search(result: dict) -> dict:
		id = result.get('id')
		alt = result.get('title')
		url = result.get('url')
		thumb = result.get('thumbnail')

		template = {
			"id": id,
			"alt_description": alt,
			"urls": {
				"full": url,
				"thumb": thumb
			}
		}

		return template


	@timed
	@add_all_args_to_self
	def search(
		self, 
		query: str, 
		per_page: int, 
		page_num: int,
		license_type: str = 'all',
		**additional_data
		) -> dict:

		results  = self._make_request()['results']
		response = [self._template_search(result) for result in results]

		return self._response.search(results=response, additional_data=additional_data)
	

	# def run(self, keywords, output_name):
	# 	all_data = []

	# 	queries = keywords.split(',')

	# 	for query in tqdm(queries, desc='queries'):
	# 		search_results = self.run_ccsearch(query, self.license_type, self.per_page, self.search_limit)
	# 		all_data.extend(search_results)

	# 	if self.return_raw_data == True:
	# 		df = pd.DataFrame(all_data)
	# 	else:
	# 		df = self.parse_ccsearch_into_upload_csv(all_data)

	# 	df.to_csv(output_name, index=False)
	# 	print(f'Output csv saved to: {output_name}')
	# 	print(
	# 			"** Note: When uploading these to an app, do so at a slower rate than normal. They seem to timeout often."
	# 	)

	# def run_ccsearch(self, query, license_type, per_page, search_limit):
	# 	'''
	# 	Input:
	# 		• query 				> search query
	# 		• license_type	> options are "commercial", "modification", "commercial,modification", or "all"
	# 		• per_page			> number of results to return per search. limit 1 - 500
	# 		• search_limit	> default and max 10000. can lower if you want less results.
	# 	Output:
	# 		• list of dicts of search results
	# 	'''
	# 	base_url = 'http://api.creativecommons.engineering/v1/images/?'

	# 	probe_search_url = f'{base_url}q={query}&license_type={license_type}&page_size=1'
	# 	probe_search_res = requests.request("GET", probe_search_url)
	# 	result_count = probe_search_res.json()['result_count']

	# 	if search_limit < result_count:
	# 		result_count = search_limit

	# 	if result_count < per_page:
	# 		per_page = result_count

	# 	search_results = []

	# 	error_count = 0

	# 	try:
	# 		for page_num in tqdm(range(0, int(np.ceil(result_count / per_page))), desc=f'results for {query}'):
	# 			search_url = f'{base_url}q={query}&license_type={license_type}&page_size={per_page}&page={page_num}'
	# 			search_res = requests.request("GET", search_url)

	# 			if search_res.status_code == 200:
	# 				results = search_res.json()['results']
	# 				_ = [x.update({'search_query': query}) for x in results]
	# 				search_results.extend(results)
	# 			else:
	# 				if error_count < 3:
	# 					error_count += 1
	# 					time.sleep(1)
	# 					continue
	# 				else:
	# 					print(
	# 						f"There's been frequent errors with this search. Stopping with current query [{query}]."
	# 					)
	# 				return search_results

	# 	except ZeroDivisionError:
	# 		print(f"This query [{query}] resulted in zero results. skipping the query")

	# 	# below used to filter out duplicate entries
	# 	search_results = list({v['id']: v for v in search_results}.values())

	# 	return search_results


	# def parse_ccsearch_into_upload_csv(self, search_results):
	# 	'''
	# 	Input:
	# 		• "search_results"	> the list of jsons from run_ccsearch
	# 		• "query" 					> the original query term for the above
	# 	Output:
	# 		a pandas dataframe with ["url", "metadata"]
	# 			• "url"				> the direct image url
	# 			• "metadata"	> any additional info about the result from the ccsearch, usually:
	# 				• creator, creator_url, id, license, license_version, source, title, search_query
	# 	'''

	# 	df_orig = pd.DataFrame(search_results)

	# 	# keep some of the columns as metadata
	# 	columns = [
	# 			'creator', 'creator_url', 'id', 'license', 'license_version', 'source', 'title',
	# 			'search_query'
	# 	]
	# 	df_orig['metadata'] = df_orig[columns].to_dict(orient='records')

	# 	for i, each in df_orig.iterrows():
	# 		df_orig['metadata'].iat[i] = json.dumps(each['metadata'])

	# 	df_new = df_orig[['url', 'metadata']]

	# 	return df_new
			
