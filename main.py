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
    pcb = cq.importers.importStep("input/example.step")
    socket = (
        cq.importers.importStep("input/choc_socket.STEP")
        .rotateAboutCenter((1, 0, 0), 90)
    )

    assembly: cq.assembly = (
        cq.Assembly()
        .add(pcb, name="pcb", color=cq.Color("green"), loc=cq.Location(cq.Vector(-100, 100, 0)))
    )

    # TODO hardcoded for now, get from config
    padding = 17
    spread = 18

    for (zone_key, zone_value) in ergogen_config["points"]["zones"].items():
        stagger = 0
        for i, (column_key, column_value) in enumerate(zone_value["columns"].items()):
            stagger += column_value["key"].get("stagger", 0)
            for j, (row_key, row_value) in enumerate(zone_value["rows"].items()):
                assembly = assembly.add(socket, name=f"{zone_key}_{column_key}_{row_key}_socket",
                                        color=cq.Color("black"),
                                        loc=cq.Location(
                                            cq.Vector(i * spread + 7.6, j * padding + stagger + 8.75, -1.85)))
    # TODO have sockets placed on Z axis with constraints
    return assembly


# TODO get input_file as input from user
input_file = "input/example.yaml"
ergogen_config = read_ergogen_file(input_file)
result = generate_case(ergogen_config)

if __name__ == '__main__':
    output_location = "output"
    os.makedirs(output_location, exist_ok=True)
    result.export(f"{output_location}/case.stl")
    # result.toCompound().export(f"{output_location}/case.svg")
