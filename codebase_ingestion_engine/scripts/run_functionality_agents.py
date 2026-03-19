import sys
import os

BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)
sys.path.insert(0, BASE_DIR)

from src.agents.agent_runner import AgentRunner


def main():

    runner = AgentRunner(
        ast_dir="data/ast",
        semantic_index_path="data/semantic/semantic_index.json",
        traceability_path="data/traceability/traceability_graph.json",
        repo_structure_path="data/repo_scan/repo_structure.json"
    )

    runner.run()


if __name__ == "__main__":
    main()