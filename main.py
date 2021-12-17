from igramscraper.instagram import Instagram
from clarifai_scrapers import (
    CCsearch, Piqsels, 
    Pixabay, Reddit, 
    InstagramScraper
)

import json, time


def main():    
    scraper = CCsearch()

    data = scraper.search(query="grass", page_num=1, per_page=25)

    print(data)
    

if __name__ == "__main__":
    main()