import json
from pathlib import Path


class TraceabilityBuilder:

    def __init__(self, ast_dir, output_file):

        self.ast_dir = Path(ast_dir)
        self.output_file = Path(output_file)

        self.nodes = []
        self.edges = []

    def build(self):

        for file in self.ast_dir.rglob("*.json"):

            self._process_file(file)

        graph = {
            "nodes": self.nodes,
            "edges": self.edges
        }

        self.output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(self.output_file, "w") as f:
            json.dump(graph, f, indent=2)
        

    def _process_file(self, file):

        with open(file) as f:
            data = json.load(f)

        file_path = data["file_path"]

        self._add_node(file_path, "file")

        # Classes

        for cls in data.get("classes", []):

            class_id = f"{file_path}.{cls['name']}"

            self._add_node(class_id, "class")

            self._add_edge("DEFINES", file_path, class_id)

            for method in cls.get("methods", []):

                method_id = f"{class_id}.{method['name']}"

                self._add_node(method_id, "method")

                self._add_edge("DEFINES", class_id, method_id)

        # Functions

        for fn in data.get("functions", []):

            fn_id = f"{file_path}.{fn['name']}"

            self._add_node(fn_id, "function")

            self._add_edge("DEFINES", file_path, fn_id)

        # Imports

        for imp in data.get("imports", []):

            module = imp["import"]

            self._add_node(module, "module")

            self._add_edge("IMPORTS", file_path, module)

    def _add_node(self, node_id, node_type):

        self.nodes.append({
            "id": node_id,
            "type": node_type
        })

    def _add_edge(self, relation, source, target):

        self.edges.append({
            "type": relation,
            "from": source,
            "to": target
        })