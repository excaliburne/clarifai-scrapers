from clarifai_scrapers import (
    CCsearch, Piqsels, 
    Pixabay, Reddit, 
    InstagramScraper
)

import json, time


def main():    
    scraper = Piqsels()

    data = scraper.search(query="grass", page_num=1, per_page=30)

    print(data)
    

if __name__ == "__main__":
    main()