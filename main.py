from clarifai_scrapers import CCsearch, PiqselsScraper, Pixabay, Reddit

import json, time

def main():    
    scraper = Reddit()
    print(scraper.search_images(subreddit='pics', per_page=30, page=1))

if __name__ == "__main__":
    main()