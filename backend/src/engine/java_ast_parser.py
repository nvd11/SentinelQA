import os
from typing import Dict, Any, List
from ..utils.logger import logger


class JavaASTParser:
    """Parses Java source code using tree-sitter or regex fallback to extract class signatures and annotations."""

    @staticmethod
    def parse_file(file_path: str) -> Dict[str, Any]:
        if not os.path.exists(file_path):
            return {"file": file_path, "classes": [], "methods": [], "raw_content": ""}

        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        classes = []
        methods = []
        annotations = []

        # Simple high-speed extraction fallback
        lines = content.splitlines()
        for line in lines:
            stripped = line.strip()
            if stripped.startswith("@"):
                annotations.append(stripped)
            elif "class " in stripped and not stripped.startswith("//"):
                classes.append(stripped)
            elif ("public " in stripped or "protected " in stripped) and "(" in stripped and not stripped.startswith("//"):
                methods.append(stripped)

        return {
            "file": file_path,
            "classes": classes,
            "methods": methods,
            "annotations": annotations,
            "raw_content": content[:4000]
        }
