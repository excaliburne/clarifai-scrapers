"""
Non module specific tests
"""

from clarifai_scrapers import (
    CCsearch, Reddit,
    InstagramScraper, Pixabay,
    Piqsels
)

# UTILS
from clarifai_scrapers.config import Config



def _get_scrapers() -> list:

    scrapers = [
        {
            'name': 'ccsearch',
            'init': CCsearch(),
            'search_attribute': 'search'
        },
        {
            'name': 'reddit',
            'init': Reddit().submissions,
            'search_attribute': 'search'
        },
        {
            'name': 'instagram',
            'init': InstagramScraper(),
            'search_attribute': 'search_media_by_hashtag'
        }, 
        {
            'name': 'pixabay',
            'init': Pixabay(Config().get('API_KEY_PIXABAY')),
            'search_attribute': 'search'
        }, 
        {
            'name': 'piqsels',
            'init': Piqsels(),
            'search_attribute': 'search'
        }
    ]

    return scrapers
    


def test_all_search_sanity_check():
    """
    Checks if...
        - All modules returns results that are not None and correspond to requests page size
    """

    per_page = 25

    for scraper in _get_scrapers():
        req     = getattr(scraper['init'], scraper['search_attribute'])
        results = req(query="stadium", page_num=1, per_page=per_page)['results']

        if scraper['name'] != 'reddit': 
            assert len(results) > 0
            assert len(results) == per_page
    
    reddit_res = Reddit().submissions.search(query="pics", page_num=1, per_page=per_page)['results']
    assert len(reddit_res) > 0
    assert len(reddit_res) == per_page


def test_all_search_templates_format():
    """
    Checks if...
        - All response template have the required dict keys
    """

    per_page = 5

    for scraper in _get_scrapers():
        req                 = getattr(scraper['init'], scraper['search_attribute'])
        results             = req(query="stadium", page_num=1, per_page=per_page)['results']
        dict_keys_should_be = ['id', 'alt_description', 'urls']

        for key in dict_keys_should_be:
            assert all(key in result.keys() for result in results)