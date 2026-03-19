import json
from pathlib import Path


class FunctionalASTExtractor:

    def __init__(self, output_dir):

        self.output_dir = Path(output_dir) / "files"
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save_file_ast(self, file_path, data):

        # convert python file -> json
        json_path = Path(file_path).with_suffix(".json")

        output = self.output_dir / json_path

        # IMPORTANT: ensure nested folders exist
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)