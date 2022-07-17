from clarifai_scrapers import (
    CCsearch, Piqsels, 
    Pixabay, Reddit, 
    InstagramScraper
)


def main():    
    scraper = Reddit()

    data = scraper.submissions.search(query="forsen", page_num=1, per_page=25)

    print(data)
    

if __name__ == "__main__":
    main()