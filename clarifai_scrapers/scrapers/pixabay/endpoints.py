

SEARCH_PHOTO = lambda key, query, page, per_page: \
f'https://pixabay.com/api/?key={key}&q={query}&image_type=photo&page={page}&per_page={per_page}'