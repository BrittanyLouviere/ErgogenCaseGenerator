import os

import cadquery as cq

from process_config import read_ergogen_file, substitute_units


# run `cq-editor main.py` in terminal and open this file in it for debugging

# units in mm
def generate_case(ergogen_config: dict) -> cq.Assembly:
    pcb = cq.importers.importStep("input/example.step")
    socket = (
        cq.importers.importStep("input/choc_socket.STEP")
        .rotateAboutCenter((1, 0, 0), 90)
    )

    assembly: cq.assembly = (
        cq.Assembly()
        .add(pcb, name="pcb", color=cq.Color("green"), loc=cq.Location(cq.Vector(-100, 100, 0)))
    )

    default_stagger = ergogen_config['units'].get('$default_stagger', 0)
    default_spread = ergogen_config['units'].get('$default_spread', substitute_units('u', ergogen_config['units']))
    default_splay = ergogen_config['units'].get('$default_splay', 0)
    default_height = ergogen_config['units'].get('$default_height', substitute_units('u-1', ergogen_config['units']))
    default_width = ergogen_config['units'].get('$default_width', substitute_units('u-1', ergogen_config['units']))
    default_padding = ergogen_config['units'].get('$default_padding', substitute_units('u', ergogen_config['units']))
    default_autobind = ergogen_config['units'].get('$default_autobind', 10)

    for (zone_key, zone_value) in ergogen_config["points"]["zones"].items():
        stagger = float(substitute_units(zone_value['key'].get('stagger', default_stagger), ergogen_config['units']))
        spread = float(substitute_units(zone_value['key'].get('spread', default_spread), ergogen_config['units']))
        splay = float(substitute_units(zone_value['key'].get('splay', default_splay), ergogen_config['units']))
        height = float(substitute_units(zone_value['key'].get('height', default_height), ergogen_config['units']))
        width = float(substitute_units(zone_value['key'].get('width', default_width), ergogen_config['units']))
        padding = float(substitute_units(zone_value['key'].get('padding', default_padding), ergogen_config['units']))
        autobind = float(substitute_units(zone_value['key'].get('autobind', default_autobind), ergogen_config['units']))

        stagger = 0
        for i, (column_key, column_value) in enumerate(zone_value["columns"].items()):
            stagger += column_value.get("key", {}).get("stagger", 0)
            for j, (row_key, row_value) in enumerate(zone_value["rows"].items()):
                if not column_value.get("rows", {}).get(row_key, {}).get("skip", False):
                    assembly = assembly.add(socket,
                                            name=f"{zone_key}_{column_key}_{row_key}_socket",
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
