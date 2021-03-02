from clarifai_scrapers import CCsearch, PiqselsScraper, Pixabay, Reddit, InstagramScraper

import json, time

def main():    
    scraper = Reddit()

    print(json.dumps(scraper.run_scraper(subreddit='pics', limit=20), indent=4))
    

if __name__ == "__main__":
    main()