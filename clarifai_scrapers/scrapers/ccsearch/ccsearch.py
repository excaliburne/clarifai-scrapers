# SYSTEM IMPORTS
import json, datetime, os
from pathlib import Path

# MODULES
from clarifai_scrapers.scrapers.base import ScraperBase

# ERRORS
from clarifai_scrapers.errors import FailedAuthentication, AuthenticationRequired

# UTILS
from clarifai_scrapers.utils.decorators import add_all_args_to_self, timed
from clarifai_scrapers.utils.http       import call_curl

# CONSTS
from .endpoints import SEARCH_IMAGES_URL


def current_time():
	return int(datetime.datetime.now().timestamp())


class CCsearch(ScraperBase):

	def __init__(self, auth_object: dict = None):
		"""

		Args:
			auth_object (dict, optional): Necessary if you want to request from than 30 images per page
				{'client_id': '', 'client_secret': ''}
		"""
		super().__init__()

		self.license_type = 'all'
		self.query        = ''
		self.page         = 1
		self.per_page     = 20

		self.auth_object  = auth_object
		
		if auth_object and self._is_token_expired():
			self._create_access_token()
	
	# -- AUTH -- #
	def _create_access_token(self) -> dict:
		url = 'https://api.openverse.engineering/v1/auth_tokens/token/'
		client_id, client_secret = self.auth_object.values()
		current_directory = Path(__file__).resolve().parent

		curl_cmd = f'''curl \
			-X POST \
			-d "client_id={client_id}&client_secret={client_secret}&grant_type=client_credentials" \
			"{url}"
		'''

		response = call_curl(curl_cmd)

		if response.get('access_token') is not None:
			with open(f'{current_directory}/oauth.json', 'w') as oauth_file:
				expiration_time = datetime.datetime.now() + datetime.timedelta(seconds=response['expires_in'])
				data_to_dump = {
					**response,
					'expiration_date': int(expiration_time.timestamp())
				}
				json.dump(data_to_dump, oauth_file)
		else:
			raise FailedAuthentication('CCsearch')
		
		return response


	def _get_access_token_object(self) -> dict:
		current_directory   = Path(__file__).resolve().parent
		access_token_object = None

		with open(f'{current_directory}/oauth.json', 'r') as oauth_file:
			oauth_content       = json.load(oauth_file)
			access_token_object = oauth_content

		return access_token_object
	

	def _is_token_expired(self) -> bool:
		if not self._oauth_file_exists():
			return True
		else:
			return current_time() > self._get_access_token_object()['expiration_date']


	def _oauth_file_exists(self) -> bool:
		current_directory = Path(__file__).resolve().parent

		return os.path.exists(f'{current_directory}/oauth.json')


	# -- OTHER -- #
	def _make_request(self) -> dict: 
		params = {
            'query': self.query,
            'page_num': self.page,
			'per_page': self.per_page,
			'license_type': self.license_type
        }
		access_token = self._get_access_token_object().get('access_token')
		headers      = {}

		if access_token and self.auth_object:
			headers['Authorization'] = f'Bearer {access_token}'

		url      = self._url_handler.build(SEARCH_IMAGES_URL, params)
		response = self._http_client.make_request("GET", url, additionalHeaders=headers)
		
		return response.json()


	@staticmethod
	def _template_search(result: dict) -> dict:
		id    = result.get('id')
		alt   = result.get('title')
		url   = result.get('url')
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
		page: int = 1,
		per_page: int = 30, 
		license_type: str = 'all',
		**additional_data
		) -> dict:

		# TODO: could make this a decorator
		if not self.auth_object and per_page > 20:
			raise AuthenticationRequired('Authentication is required to query page size > 20')

		results  = self._make_request().get('results') or []
		response = [self._template_search(result) for result in results]

		return self._response.returns(response)
