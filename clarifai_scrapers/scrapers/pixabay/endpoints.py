from clarifai_scrapers.scrapers.reddit.endpoints import BASE_URL


BASE_URL = 'https://pixabay.com/api/'

SEARCH_IMAGES_URL = BASE_URL + '?key={api_key}&q={query}&image_type=photo&page={page_num}&per_page={per_page}'