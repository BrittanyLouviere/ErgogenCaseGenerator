import yaml


def read_ergogen_file(file_path: str) -> dict:
    with open(file_path) as stream:
        config = yaml.safe_load(stream)
    config = expand_keys(config)
    return config


def expand_keys(dictionary: dict) -> dict:
    newDictionary = {}
    for key, value in dictionary.items():
        val = expand_keys(value) if type(value) is dict else value
        if '.' in key:
            key1, key2 = key.split('.', 1)
            newDictionary[key1] = {key2: val}
        else:
            newDictionary[key] = val
    return newDictionary
