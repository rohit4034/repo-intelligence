from pathlib import Path

from src.plugins.python.python_parser import PythonParser
from src.plugins.python.python_ast_extractor import PythonASTExtractor
from src.core.ast_engine.functional_ast_extractor import FunctionalASTExtractor


class ASTBuilder:

    def __init__(self, ast_output_dir):

        self.parser = PythonParser()
        self.extractor = PythonASTExtractor()
        self.saver = FunctionalASTExtractor(ast_output_dir)

    def process_file(self, file_path, repo_root):

        tree, source = self.parser.parse(file_path)
        root = tree.root_node

        relative_path = str(Path(file_path).relative_to(repo_root))

        data = {
            "repository": Path(repo_root).name,
            "module": self._module_name(relative_path),
            "file_path": relative_path,
            "classes": [],
            "functions": [],
            "methods": [],
            "imports": [],
            "calls": []
        }

        self.extractor.extract(root, source, data)

        self.saver.save_file_ast(relative_path, data)

    def _module_name(self, path):

        return path.replace("/", ".").replace(".py", "")