

def filter(dict_, keys_to_keep):
    return {key: dict_[key] for key in keys_to_keep if key in dict_}