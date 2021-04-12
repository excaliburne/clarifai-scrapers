def convert_to_scrape_format(all_data):
    for item in all_data:
        filtered_metadata = {}
        url = ''
        for k, v in item.items():
            if k in ('alt_description', 'id'):
                filtered_metadata.update({k: v})

        item['url'] = item['urls']['full']
        item['metadata'] = filtered_metadata
        item['concepts'] = []
        del item['alt_description']
        del item['id']
        del item['urls']

    return all_data


        