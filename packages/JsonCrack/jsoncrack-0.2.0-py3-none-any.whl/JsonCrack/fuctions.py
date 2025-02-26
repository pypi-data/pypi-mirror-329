from JsonCrack.__init__ import *
def visualize(data, output_file, display,silent):
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
                if not silent:
                    print(f"Unsupported OS: {os_type}")
        else:
            if not silent:
                print(f"Error: PNG file not found! Expected at {file_path}")
    if not silent:
        print(f"{file_path} Saved Successfully")
    if display and not silent:
        print(f"{file_path} Displayed Successfully")

def convert_js_to_python(data:str):
    data = data.replace("None", "null").replace("False", "false").replace("True", "true")
    """Convert JavaScript-like JSON to Python-compatible JSON."""
    return json.loads(
        data,
        parse_constant=lambda x: {"null": None, "false": False, "true": True}.get(x, x),
    )
class CodeDictionaryMapper:
    def __init__(self, filename="code_mapping.json"):
        self.filename = filename
        self.load_data()

    def generate_code(self):
        """Generate a unique 10-digit alphanumeric code."""
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
            if code not in self.code_to_dict:
                return code

    def load_data(self):
        """Load stored data from JSON file."""
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                data = json.load(file)
                self.code_to_dict = data.get("code_to_dict", {})
                self.dict_to_code = {frozenset(eval(k)): v for k, v in data.get("dict_to_code", {}).items()}
        else:
            self.code_to_dict = {}
            self.dict_to_code = {}

    def save_data(self):
        """Save mappings to JSON file."""
        with open(self.filename, "w") as file:
            json.dump({
                "code_to_dict": self.code_to_dict,
                "dict_to_code": {str(k): v for k, v in self.dict_to_code.items()}
            }, file)

    def freeze_dict(self, d):
        """ Recursively converts a dictionary into an immutable structure (frozenset). """
        if isinstance(d, dict):
            return frozenset((key, self.freeze_dict(value)) for key, value in d.items())
        elif isinstance(d, list):
            return tuple(self.freeze_dict(item) for item in d)  # Convert lists to tuples
        return d  # Leave other types unchanged
    def add_entry(self, data_dict):
        """Add a dictionary and generate a unique code for it."""
        #data_dict_frozen = frozenset(data_dict.items())  # Convert dict to immutable format
        data_dict_frozen = self.freeze_dict(data_dict)  # Freeze dictionary recursively
        if data_dict_frozen in self.dict_to_code:
            return self.dict_to_code[data_dict_frozen]  # Return existing code

        code = self.generate_code()
        self.code_to_dict[code] = data_dict  # Store dictionary
        self.dict_to_code[data_dict_frozen] = code  # Store reverse lookup
        self.save_data()  # Save to file
        return code

    def get_dict_by_code(self, code):
        """Retrieve dictionary by code."""
        return self.code_to_dict.get(code)

    def get_code_by_dict(self, data_dict):
        """Retrieve code by dictionary."""
        return self.dict_to_code.get(frozenset(data_dict.items()))