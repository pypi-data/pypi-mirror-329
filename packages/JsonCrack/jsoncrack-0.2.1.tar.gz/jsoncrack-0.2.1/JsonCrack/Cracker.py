from JsonCrack.fuctions import *

class JSON:
    def __init__(self, data):
        self.data = data
    def visualize(self, output_file="visualize_output", display=True,silent=False):
        return visualize(self.data, output_file, display,silent=silent)
    def convert_js_to_python(self):
        self.data = convert_js_to_python(self.data)
        return self.data


