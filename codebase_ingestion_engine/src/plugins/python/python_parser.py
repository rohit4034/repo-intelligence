from tree_sitter import Parser, Language
import tree_sitter_python as tspython


class PythonParser:

    def __init__(self):

        self.parser = Parser()

        # Convert capsule → Language object
        PY_LANGUAGE = Language(tspython.language())

        self.parser.language = PY_LANGUAGE

    def parse(self, file_path):

        with open(file_path, "rb") as f:
            source = f.read()

        tree = self.parser.parse(source)

        return tree, source