from JsonCrack.__init__ import *
def visualize(data, output_file, display):
    """
    Visualizes a JSON structure as a vertical graph.

    :param data: JSON data (dict or list).
    :param output_file: Name of the output file (without extension).
    :param display: If True, displays the generated visualization.
    :param save: If True, saves the visualization as a file.
    """
    dot = graphviz.Digraph(format="png")

    def add_nodes_edges(obj, parent=None):
        if isinstance(obj, dict):
            for key, value in obj.items():
                node_id = f"{key}_{id(value)}"
                dot.node(node_id, label=key, shape="box")
                if parent:
                    dot.edge(parent, node_id)
                add_nodes_edges(value, node_id)
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                node_id = f"{parent}_{i}"
                dot.node(node_id, label=f"[{i}]", shape="ellipse")
                dot.edge(parent, node_id)
                add_nodes_edges(item, node_id)
        else:
            leaf_id = f"{parent}_value"
            dot.node(leaf_id, label=str(obj), shape="oval", color="gray")
            dot.edge(parent, leaf_id)

    root_id = "root"
    dot.node(root_id, label="JSON", shape="diamond", style="filled", fillcolor="lightblue")
    add_nodes_edges(data, root_id)

    file_path = dot.render(output_file)

    if display and file_path:
        if os.path.exists(file_path):
            os_type = platform.system()
            if os_type == "Windows":
                os.system(f'start {file_path}')
            elif os_type == "Darwin":  # macOS
                os.system(f'open {file_path}')
            elif os_type == "Linux":
                os.system(f'xdg-open {file_path}')
            else:
                print(f"Unsupported OS: {os_type}")
        else:
            print(f"Error: PNG file not found! Expected at {file_path}")
    print(f"{file_path} Saved Successfully")
    if display:
        print(f"{file_path} Displayed Successfully")

def convert_js_to_python(data:str):
    data = data.replace("None", "null").replace("False", "false").replace("True", "true")
    """Convert JavaScript-like JSON to Python-compatible JSON."""
    return json.loads(
        data,
        parse_constant=lambda x: {"null": None, "false": False, "true": True}.get(x, x),
    )
