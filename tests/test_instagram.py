from clarifai_scrapers import InstagramScraper



def _get_scraper():
    scraper = InstagramScraper()

    return scraper


def _run(attribute, **params):
    run = getattr(_get_scraper(), attribute)

    return run(**params)


