from clarifai_scrapers import CCsearch

import json
import requests

def main():    
    scraper = CCsearch(license_type='all', per_page=30, search_limit=300, return_raw_data=False)    
    keywords="stadium"
    default_output = "~/Downloads/ccsearch.csv"

    json_data = scraper.search(query="beach", size=30, page_num=4)
    print(json.dumps(json_data, indent=2))


if __name__ == "__main__":
    main()