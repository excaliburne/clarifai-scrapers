from clarifai_scrapers import CCsearch, PiqselsScraper, Pixabay, Reddit, InstagramScraper

import json, time

def main():    
    scraper = InstagramScraper()

    print(json.dumps(scraper.search_media_by_hashtag(hashtag='sky', count=10, page=1), indent=4))
    

if __name__ == "__main__":
    main()