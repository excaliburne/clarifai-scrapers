from clarifai_scrapers import CCsearch

import json

def main():    
    scraper = CCsearch(license_type='all', per_page=10, search_limit=30, return_raw_data=False)    
    keywords="potato,chips"
    default_output = "~/Downloads/ccsearch.csv"

    json_data = scraper.run(keywords, default_output, return_formatted_dict=True)
    print(json.dumps(json_data, indent=2))


if __name__ == "__main__":
    main()