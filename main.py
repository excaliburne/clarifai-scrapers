from clarifai_scrapers import (
    CCsearch, PiqselsScraper, 
    Pixabay, Reddit, 
    InstagramScraper
)

import json, time


def main():    
    scraper = Pixabay('19656232-d9688ba6bdcd8dd2414f9e132')

    print(json.dumps(scraper.search(query="stadium", page_num=1, per_page=30), indent=4))
    

if __name__ == "__main__":
    main()