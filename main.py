from clarifai_scrapers import CCsearch, InstagramScaper, PiqselsScraper

import json
import requests

import time


def main():    
    scraper = PiqselsScraper()

    data = scraper.scrape(query='plane', page_num=1, per_page=30)
    print(json.dumps(data, indent=2))
   

if __name__ == "__main__":
    main()