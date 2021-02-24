from clarifai_scrapers import CCsearch, PiqselsScraper, Pixabay, Reddit

import json, time

def main():    
    scraper = Reddit()
    print(scraper.run_scraper(
        subreddit='pics',
        limit=4
        # output_file='~/Downloads/reddit5.csv'
    ))

if __name__ == "__main__":
    main()