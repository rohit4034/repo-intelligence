import json
import logging
from pathlib import Path


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


class FunctionalityDescriptionGenerator:

    def __init__(
        self,
        ast_dir,
        semantic_index_path,
        traceability_path,
        repo_structure_path,
        llm_client
    ):

        logger.info("Initializing FunctionalityDescriptionGenerator")

        self.ast_dir = Path(ast_dir)
        self.llm = llm_client

        logger.info(f"AST directory: {self.ast_dir}")

        logger.info("Loading semantic index")
        with open(semantic_index_path) as f:
            self.semantic_index = json.load(f)

        logger.info("Loading traceability graph")
        with open(traceability_path) as f:
            self.traceability = json.load(f)

        logger.info("Loading repo structure")
        with open(repo_structure_path) as f:
            self.repo_structure = json.load(f)

        logger.info("Initialization complete")


    def run(self):

        logger.info("Starting functionality description generation")

        ast_files = list(self.ast_dir.rglob("*.json"))

        logger.info(f"Found {len(ast_files)} AST files")

        for ast_file in ast_files:

            logger.info(f"Processing AST file: {ast_file}")

            with open(ast_file) as f:
                ast_data = json.load(f)

            # Ensure file context exists
            if "file" not in ast_data:
                ast_data["file"] = ast_file.relative_to(self.ast_dir).as_posix()

            self._process_file(ast_data)

        logger.info("Completed functionality generation")


    def _process_file(self, ast_data):

        file_name = ast_data["file"]

        logger.info(f"Generating functionality for file: {file_name}")

        functions = ast_data.get("functions", [])
        methods = ast_data.get("methods", [])

        logger.info(f"Functions in file: {len(functions)}")
        logger.info(f"Methods in file: {len(methods)}")

        entities = []

        for fn in functions:
            entities.append({
                "type": "function",
                "name": fn["name"],
                "class": None,
                "code": fn["code"]
            })

        for method in methods:
            entities.append({
                "type": "method",
                "name": method["name"],
                "class": method.get("class"),
                "code": method["code"]
            })

        capability_input = {
            "repository_context": self.repo_structure,

            "file_context": {
                "file": file_name,
                "imports": ast_data["imports"]
            },

            "entities": entities,

            "semantic_metadata": self.semantic_index.get(
                file_name, {}
            ),

            "traceability": self._traceability_for_file(entities)
        }

        prompt_input = json.dumps(capability_input, indent=2)

        from src.core.llm.prompt_manager import (
            _SYSTEM_PROMPT_PHASE1,
            build_prompt
        )

        user_prompt = build_prompt(prompt_input)

        logger.info(f"Sending file-level request to LLM: {file_name}")

        result = self.llm.generate(
            _SYSTEM_PROMPT_PHASE1,
            user_prompt
        )

        logger.info(f"Received LLM response for file: {file_name}")

        self._save(file_name, result)


    def _traceability_context(self, name):

        logger.debug(f"Building traceability context for {name}")

        calls = []
        called_by = []

        for edge in self.traceability["edges"]:

            if edge["type"] == "CALLS":

                if edge["from"] == name:
                    calls.append(edge["to"])

                if edge["to"] == name:
                    called_by.append(edge["from"])

        return {
            "calls": calls,
            "called_by": called_by
        }
    def _traceability_for_file(self, entities):

        entity_names = {e["name"] for e in entities}

        calls = []

        for edge in self.traceability["edges"]:

            if edge["type"] == "CALLS":

                if edge["from"] in entity_names or edge["to"] in entity_names:

                    calls.append(edge)

        return {
            "edges": calls
        }

    def _save(self, file_name, data):

        out = Path("data/functionality_descriptions")
        out.mkdir(exist_ok=True)

        safe_name = file_name.replace("/", "_").replace(".json", "")

        path = out / f"{safe_name}.json"

        logger.info(f"Saving functionality description: {path}")

        with open(path, "w") as f:
            json.dump(data, f, indent=2)