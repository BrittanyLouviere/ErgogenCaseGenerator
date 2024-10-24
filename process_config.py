import ast
import operator as op

import yaml


def read_ergogen_file(file_path: str) -> dict:
    with open(file_path) as stream:
        config = yaml.safe_load(stream)
    config = calculate_units(config)
    config = expand_keys(config)
    return config


def expand_keys(dictionary: dict) -> dict:
    new_dictionary = {}
    for key, value in dictionary.items():
        val = expand_keys(value) if type(value) is dict else value
        if '.' in key:
            key1, key2 = key.split('.', 1)
            new_dictionary[key1] = {key2: val}
        else:
            new_dictionary[key] = val
    return new_dictionary


def substitute_units(value: str, units: dict) -> str:
    new_val = value
    subbed = False
    for (key2, value2) in units.items():
        if key2 in new_val:
            subbed = True
            index = new_val.find(key2) - 1
            new_val = (
                ("*" + str(value2)).join(new_val.split(key2))
                if index >= 0 and new_val[index].isnumeric()
                else new_val.replace(key2, str(value2))
            )
    return eval_expr(new_val) if subbed else new_val


def calculate_units(dictionary: dict) -> dict:
    new_units = {
        'U': 19.05,  # 19.05mm MX spacing
        'u': 19,  # 19mm MX spacing
        'cx': 18,  # 18mm Choc X spacing
        'cy': 17,  # 17mm Choc Y spacing
    }
    for (key, value) in dictionary['units'].items():
        if isinstance(value, (int, float, complex)):
            new_units[key] = value
        elif isinstance(new_val := substitute_units(str(value), new_units), (int, float, complex)):
            new_units[key] = new_val
        else:
            new_units[key] = eval_expr(new_val)
    dictionary['units'] = new_units
    return dictionary


# supported operators
operators = {ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul,
             ast.Div: op.truediv, ast.Pow: op.pow, ast.BitXor: op.xor,
             ast.USub: op.neg}


def eval_expr(expr):
    return eval_(ast.parse(expr, mode='eval').body)


def eval_(node):
    match node:
        case ast.Constant(value) if isinstance(value, (int, float, complex)):
            return value
        case ast.BinOp(left, op, right):
            return operators[type(op)](eval_(left), eval_(right))
        case ast.UnaryOp(op, operand):  # e.g., -1
            return operators[type(op)](eval_(operand))
        case _:
            raise TypeError(node)
