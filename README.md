❗ Incoming a proper README! This is still being developped and structure is chanding regularly.

# Supports...
### Instagram
- [X] Search
- [ ] Scrape

### Reddit
- [X] Search
- [X] Scrape

### CCsearch (Auth optional but recommended)
- [X] Search
- [ ] Scrape

### Pixabay (Requires auth)
- [X] Search
- [ ] Scrape

### Unsplash (Requires auth)
- [X] Search
- [ ] Scrape

### Piqsels
- [X] Search
- [ ] Scrape
### Pexels (Requires auth)
- [ ] Search
- [ ] Scrape

### VisualHunt (https://visualhunt.com/)
- [ ] Search
- [ ] Scrape

### Freephotos.cc 
- [ ] Search
- [ ] Scrape

### iStockPhoto
- [ ] Search
- [ ] Scrape

### Flickr (Requires auth)
- [ ] Search 
- [ ] Scrape


# Usage
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

# Response Schema
## Success
```json
[
    {
        "id": "...",
        "alt_description": "...",
        "urls": {
            "full": "...",
            "thumb": "..."
        }
    }
]
```
## Failure or no inputs found/fetched
```json
[]
```
