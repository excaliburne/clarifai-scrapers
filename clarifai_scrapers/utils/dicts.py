def delete_none_values(dictt: dict):
    new_dict = {key: value for (key, value) in dictt.items() if value is not None}

    return new_dict