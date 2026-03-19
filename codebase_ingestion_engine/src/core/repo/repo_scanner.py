import os
from pathlib import Path
from typing import List, Dict

SUPPORTED_LANGUAGES = {
    ".py": "python"
}

DEFAULT_IGNORE_DIRS = {
    ".git",
    "__pycache__",
    "venv",
    "node_modules",
    ".idea",
    ".vscode",
    "dist",
    "build"
}


class RepoScanner:
    def __init__(
        self,
        repo_path: str,
        ignore_dirs: set = None
    ):
        self.repo_path = Path(repo_path)
        self.ignore_dirs = ignore_dirs or DEFAULT_IGNORE_DIRS

    def scan(self) -> Dict:
        """
        Scan repository and return file metadata
        """
        repo_structure = {
            "repo_root": str(self.repo_path),
            "files": []
        }

        for root, dirs, files in os.walk(self.repo_path):

            # remove ignored directories
            dirs[:] = [
                d for d in dirs
                if d not in self.ignore_dirs
            ]

            for file in files:

                file_path = Path(root) / file
                ext = file_path.suffix

                if ext not in SUPPORTED_LANGUAGES:
                    continue

                metadata = self._extract_file_metadata(file_path)

                repo_structure["files"].append(metadata)

        return repo_structure

    def _extract_file_metadata(self, file_path: Path) -> Dict:

        try:
            size = file_path.stat().st_size
            lines = self._count_lines(file_path)

        except Exception:
            size = 0
            lines = 0

        return {
            "path": str(file_path.relative_to(self.repo_path)),
            "language": SUPPORTED_LANGUAGES[file_path.suffix],
            "size": size,
            "lines": lines
        }

    def _count_lines(self, file_path: Path) -> int:
        count = 0
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            for _ in f:
                count += 1
        return count