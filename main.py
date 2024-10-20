import os

import cadquery as cq
import yaml


# run `cq-editor main.py` in terminal and open this file in it for debugging

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

# units in mm
def generate_case(ergogen_config):
    return cq.Workplane("front").box(2.0, 2.0, 0.5)


# TODO get input_file as input from user
input_file = "input/example.yaml"
ergogen_config = read_ergogen_file(input_file)
result = generate_case(ergogen_config)

if __name__ == '__main__':
    output_location = "output"
    os.makedirs(output_location, exist_ok=True)
    result.export(f"{output_location}/case.stl")
    result.export(f"{output_location}/case.svg")
