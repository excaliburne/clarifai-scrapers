BASE_URL      = 'https://api.flickr.com/services/rest'

SEARCH_PHOTOS = BASE_URL + \
    '?method=flickr.photos.search&sort=relevance&parse_tags=1&content_type=7&text={query}&page={page} \
    &extras=2Cdescription%2Cisfavorite%2Clicense%2Cmedia%2Cneeds_interstitial%2Cowner_name%2Cpath_alias \
    %2Crealname%2Crotation%2Curl_sq%2Curl_q%2Curl_t%2Curl_s%2Curl_n%2Curl_w%2Curl_m%2Curl_z%2Curl_c%2Curl_l \
    &per_page={per_page}&api_key={api_key}&format=json&hermes=1&hermesClient=1&nojsoncallback=1'