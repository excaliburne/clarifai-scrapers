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