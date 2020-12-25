from clarifai_scrapers import CCsearch, PiqselsScraper, Pixabay

import json
import requests

import time


def main():    
    scraper = Pixabay('19656232-d9688ba6bdcd8dd2414f9e132')
    data = scraper.scrape_toolbox_format(query='sky', page_num=3, per_page=30)

    print(json.dumps(data, indent=2))
   

if __name__ == "__main__":
    main()