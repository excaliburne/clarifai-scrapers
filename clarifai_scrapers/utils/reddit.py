def filter_metadata(all_data):
    for item in all_data:
        filtered_meta = {}
        for k, v in item['metadata'].items():
            if k in (
                'total_awards_received', 'content_categories',
                'upvote_ratio', 'subreddit_subscribers',
                'num_comments'
            ):
                filtered_meta.update({ k: v })

        item['concepts'] = ''
        item['not concepts'] = ''
        item['metadata'] = filtered_meta
    
    return all_data
