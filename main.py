from clarifai_scrapers import CCsearch, PiqselsScraper, Pixabay, Reddit

import json, time

def main():    
    scraper = Reddit()
    print(scraper.run_scraper(
        subreddit='pics',
        limit=110
    ))

if __name__ == "__main__":
    main()