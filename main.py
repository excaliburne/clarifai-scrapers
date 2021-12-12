from clarifai_scrapers import (
    CCsearch, PiqselsScraper, 
    Pixabay, Reddit, 
    InstagramScraper
)

import json, time


def main():    
    scraper = Reddit()

    print(json.dumps(scraper.submissions.search(subreddit="pics", per_page=30, page_num=1), indent=4))
    

if __name__ == "__main__":
    main()