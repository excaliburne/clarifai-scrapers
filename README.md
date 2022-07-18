❗ Incoming a proper README! This is still being developped and structure is chanding regularly.

### Supports...
- Instagram
    - [X] Search
    - [ ] Scrape
- Reddit
    - [X] Search
    - [X] Scrape
- CCsearch
    - [X] Search
    - [ ] Scrape
- Pixabay
    - [X] Search
    - [ ] Scrape
- Unsplash
    - [X] Search
    - [ ] Scrape
- Piqsels
    - [ ] Search
    - [ ] Scrape


### Usage
``` python
from clarifai_scrapers import (
    CCsearch, Piqsels, 
    Pixabay, Reddit, 
    InstagramScraper
)

scraper = Reddit()
data    = scraper.submissions.search(query="pics", page_num=1, per_page=25)

print(data)
```
