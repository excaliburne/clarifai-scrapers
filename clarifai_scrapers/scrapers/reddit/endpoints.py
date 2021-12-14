"""
Reddit API endpoints
"""

BASE_URL = 'https://api.pushshift.io/reddit/'

SEARCH_SUBMISSIONS_IN_SUBREDDIT_URL = BASE_URL + 'search/submission/?subreddit={subreddit}&size={per_page}{other_params}'
