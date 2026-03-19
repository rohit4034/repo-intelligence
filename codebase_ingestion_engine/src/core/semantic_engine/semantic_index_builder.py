import json
from pathlib import Path


class SemanticIndexBuilder:

    def __init__(self, ast_dir, traceability_file, output_file):

        self.ast_dir = Path(ast_dir)
        self.traceability_file = Path(traceability_file)
        self.output_file = Path(output_file)

        with open(self.traceability_file) as f:
            self.traceability = json.load(f)

    def build(self):

        semantic_index = {}

        for ast_file in self.ast_dir.rglob("*.json"):

            with open(ast_file) as f:
                ast_data = json.load(f)

            file_path = ast_data["file_path"]

            semantic_index[file_path] = self._build_file_summary(ast_data)

        self.output_file.parent.mkdir(parents=True, exist_ok=True)

        with open(self.output_file, "w") as f:
            json.dump(semantic_index, f, indent=2)

        print(f"Semantic index saved to: {self.output_file}")

    def _build_file_summary(self, ast):

        classes = []
        methods = []
        functions = []
        imports = []
        calls = []

        for cls in ast.get("classes", []):

            classes.append(cls["name"])

            for m in cls.get("methods", []):
                methods.append(m["name"])

        for fn in ast.get("functions", []):
            functions.append(fn["name"])

        for imp in ast.get("imports", []):
            imports.append(imp["import"])

        # Collect calls from traceability

        for edge in self.traceability["edges"]:

            if edge["type"] == "CALLS" and edge["from"].startswith(ast["file_path"]):

                calls.append(edge["to"])

        return {
            "classes": classes,
            "methods": methods,
            "functions": functions,
            "imports": imports,
            "calls": list(set(calls))
        }