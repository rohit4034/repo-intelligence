import json


class CapabilityBuilder:

    def __init__(self, semantic_index, traceability, repo_structure):
        self.semantic_index = semantic_index
        self.traceability = traceability
        self.repo_structure = repo_structure


    def build(self, ast_data, entity):

        name = entity["name"]

        calls = []
        called_by = []

        for edge in self.traceability["edges"]:

            if edge["type"] == "CALLS":

                if edge["from"] == name:
                    calls.append(edge["to"])

                if edge["to"] == name:
                    called_by.append(edge["from"])

        capability = {
            "repository_structure": self.repo_structure,

            "file_context": {
                "file": ast_data["file"],
                "imports": ast_data["imports"]
            },

            "entity": {
                "name": entity["name"],
                "class": entity.get("class"),
                "code": entity["code"]
            },

            "semantic_metadata": self.semantic_index.get(
                ast_data["file"], {}
            ),

            "traceability": {
                "calls": calls,
                "called_by": called_by
            }
        }

        return capability