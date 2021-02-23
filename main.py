from clarifai_scrapers import CCsearch, PiqselsScraper, Pixabay, Reddit

import json, time

def main():    
    scraper = Reddit(
        subreddit='pics'
    )
    print(scraper.search_images(per_page=30, page=1))
    print(scraper.search_images(per_page=30, page=2))
    print(scraper.search_images(per_page=30, page=3))

if __name__ == "__main__":
    main()