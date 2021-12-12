from os import scandir
from clarifai_scrapers import Pixabay

# ROOT
from clarifai_scrapers.config import Config


def _get_scraper():
    api_key = Config().get('API_KEY_PIXABAY')
    scraper = Pixabay(api_key)

    return scraper


def _run(attribute, **params):
    run = getattr(_get_scraper(), attribute)

    return run(**params)


def test_pixabay_search():
    """
    Checks if...
        - Search results is not null
        - We're receiving the correct length requested
    """
    per_page = 25
    results = _run('search', query="stadium", page_num=1, per_page=per_page)['results']
    
    assert len(results) > 0
    assert len(results) == per_page


def test_pixabay_search_output():
    """
    Checks output formart of search function
    """
    results = _run('search', query="stadium", page_num=1, per_page=5)['results']

    dict_keys_should_be = ['id', 'alt_description', 'urls']

    for res in results:
        assert sorted(res.keys()) == sorted(dict_keys_should_be)

        