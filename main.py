import cadquery as cq

# run `cq-editor` in terminal and open this file in it for debugging

def read_ergogen_file(file_path: str):
    pass

def generate_case():
    return cq.Workplane("front").box(2.0, 2.0, 0.5)

if __name__ == '__main__':
    pass

read_ergogen_file("example.yaml")
result = generate_case()