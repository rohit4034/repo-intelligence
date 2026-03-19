import json
from pathlib import Path

from src.agents.functionality_agent import FunctionalityAgent
from src.agents.capability_builder import CapabilityBuilder


class AgentRunner:

    def __init__(
        self,
        ast_dir,
        semantic_index_path,
        traceability_path,
        repo_structure_path
    ):

        with open(semantic_index_path) as f:
            semantic_index = json.load(f)

        with open(traceability_path) as f:
            traceability = json.load(f)

        with open(repo_structure_path) as f:
            repo_structure = json.load(f)

        self.builder = CapabilityBuilder(
            semantic_index,
            traceability,
            repo_structure
        )

        self.agent = FunctionalityAgent()

        self.ast_dir = Path(ast_dir)


    def run(self):

        for ast_file in self.ast_dir.rglob("*.json"):

            with open(ast_file, "r", encoding="utf-8") as f:
                ast_data = json.load(f)

            # Always inject file path
            file_path = ast_file.relative_to(self.ast_dir).as_posix()

            ast_data["file"] = file_path

            entities = (
                ast_data.get("functions", [])
                + ast_data.get("methods", [])
            )

            for entity in entities:

                capability = self.builder.build(
                    ast_data,
                    entity
                )

                result = self.agent.run(capability)

                self._save(file_path, entity["name"], result)


    def _save(self, file_name, entity_name, result):

        output_dir = Path("data/functionality_descriptions")
        output_dir.mkdir(parents=True, exist_ok=True)

        safe_file = file_name.replace("/", "_")

        filename = f"{safe_file}_{entity_name}.json"

        with open(output_dir / filename, "w", encoding="utf-8") as f:
            f.write(result)