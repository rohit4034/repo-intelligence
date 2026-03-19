import sys
import os
import json
from pathlib import Path

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, BASE_DIR)

from src.core.repo.repo_scanner import RepoScanner


repo_path = r"C:\Users\91810\repo-intelligence\test_projects\freqtrade-develop"

scanner = RepoScanner(repo_path)

repo_index = scanner.scan()

# Print output
print(json.dumps(repo_index, indent=2))


# -------- Save Output -------- #

output_path = Path(BASE_DIR) / "data" / "repo_scan" / "repo_structure.json"

# create directories if they don't exist
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w", encoding="utf-8") as f:
    json.dump(repo_index, f, indent=2)

print(f"\nRepo structure saved to: {output_path}")


from src.core.ast_engine.ast_builder import ASTBuilder
from pathlib import Path

ast_builder = ASTBuilder("data/ast")

for file in repo_index["files"]:

    if file["language"] != "python":
        continue

    file_path = Path(repo_path) / file["path"]

    ast_builder.process_file(file_path, repo_path)
    
from src.core.metadata_engine.traceability_builder import TraceabilityBuilder

builder = TraceabilityBuilder(
    ast_dir="data/ast/files",
    output_file="data/traceability/traceability_graph.json"
)

builder.build()


from src.core.semantic_engine.semantic_index_builder import SemanticIndexBuilder


semantic_builder = SemanticIndexBuilder(
    ast_dir="data/ast/files",
    traceability_file="data/traceability/traceability_graph.json",
    output_file="data/semantic/semantic_index.json"
)

semantic_builder.build()