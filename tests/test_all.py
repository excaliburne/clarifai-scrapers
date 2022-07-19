"""
Non module specific tests
"""
# SYSTEM
import pytest

# MODULES
from clarifai_scrapers import (
    CCsearch, Reddit,
    InstagramScraper, Pixabay,
    Piqsels, Unsplash
)

# ERRORS
from clarifai_scrapers.errors import PageSizeLimitExceeded

# UTILS
from clarifai_scrapers.config import Config
from clarifai_scrapers.scrapers.flickr.flickr import Flickr



def _get_scrapers() -> list:

    scrapers = [
        {
            'name': 'ccsearch',
            'init': CCsearch({
                'client_id': Config().get('CLIENT_ID_CCSEARCH'), 
                'client_secret': Config().get('CLIENT_SECRET_CCSEARCH')
            }),
            'search_attribute': 'search'
        },
        {
            'name': 'reddit',
            'init': Reddit().submissions,
            'search_attribute': 'search'
        },
        # {
        #     'name': 'instagram',
        #     'init': InstagramScraper(),
        #     'search_attribute': 'search_media_by_hashtag'
        # }, 
        {
            'name': 'pixabay',
            'init': Pixabay(Config().get('API_KEY_PIXABAY')),
            'search_attribute': 'search'
        }, 
        {
            'name': 'piqsels',
            'init': Piqsels(),
            'search_attribute': 'search'
        },
        {
            'name': 'unsplash',
            'init': Unsplash(Config().get('API_KEY_UNSPLASH')),
            'search_attribute': 'search_photos'
        },
        {
            'name': 'flickr',
            'init': Flickr(Config().get('API_KEY_FLICKR')),
            'search_attribute': 'search'
        },
    ]

    return scrapers
    


def test_all_search_sanity_check():
    """
    Checks if...
        - All modules returns results that != None and correspond to requested page size
    """
    
    PER_PAGE = 25

    for scraper in _get_scrapers():
        req     = getattr(scraper['init'], scraper['search_attribute'])
        results = req(query="stadium", page=1, per_page=PER_PAGE).get_data()

        if scraper['name'] != 'reddit': 
            assert len(results) > 0
            assert len(results) == PER_PAGE
    
    reddit_res = Reddit().submissions.search(query="pics", page=1, per_page=PER_PAGE).get_data()
    assert len(reddit_res) > 0
    assert len(reddit_res) == PER_PAGE


def test_all_search_templates_format():
    """
    Checks if...
        - All response template have the required dict keys
    """

    per_page = 5

    for scraper in _get_scrapers():
        req                 = getattr(scraper['init'], scraper['search_attribute'])
        results             = req(query="stadium", page=1, per_page=per_page).get_data()
        dict_keys_should_be = ['id', 'alt_description', 'urls']

        for key in dict_keys_should_be:
            assert all(key in result.keys() for result in results)


def test_bytes_are_refused_when_page_size_exceeds_30():
    """
    Asserts that, when a page of size > 30 is requested and user wants urls to be converted to bytes...
    ...PageSizeLimitExceeded should be raised
    """
    PER_PAGE = 50

    for scraper in _get_scrapers():
        with pytest.raises(PageSizeLimitExceeded) as excinfo:
            setattr(scraper['init'], 'also_return_bytes', True)
            req     = getattr(scraper['init'], scraper['search_attribute'])
            results = req(query="stadium", page=1, per_page=PER_PAGE).get_data()

        assert(str(excinfo.value) == 'Page size exceed limit: Bytes can only be returned when page size is <= 30')