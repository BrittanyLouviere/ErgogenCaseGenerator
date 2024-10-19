import os

import cadquery as cq
import yaml


# run `cq-editor` in terminal and open this file in it for debugging

def read_ergogen_file(file_path: str):
    with open(file_path) as stream:
        return yaml.safe_load(stream)


# units in mm
def generate_case(ergogen_config):
    return cq.Workplane("front").box(2.0, 2.0, 0.5)


# TODO get input_file as input from user
input_file = "output/example.yaml"
ergogen_config = read_ergogen_file(input_file)
result = generate_case(ergogen_config)

if __name__ == '__main__':
    output_location = "output"
    os.makedirs(output_location, exist_ok=True)
    result.export(f"{output_location}/case.stl")
    result.export(f"{output_location}/case.svg")
