import os
from typing import Optional, List
from ..utils.logger import logger
from .git_client import GitClient


class CodingStandardClient:
    """Fetches and extracts organizational coding standard rules from an external git repo."""

    def __init__(self, cache_dir: str = "/tmp/sentinelqa/standards"):
        self.cache_dir = cache_dir

    def fetch_standards(self, repo_url: Optional[str]) -> str:
        if not repo_url:
            logger.info("No department coding standard repo provided. Using default financial QA conventions.")
            return self._default_standards()

        logger.info(f"Fetching department coding standards from {repo_url}...")
        local_dest = os.path.join(self.cache_dir, "dept_standard")
        try:
            if not os.path.exists(local_dest):
                GitClient.clone_repository(repo_url, local_dest)
            return self._extract_rules_from_dir(local_dest)
        except Exception as e:
            logger.warning(f"Unable to clone coding standard repo: {e}. Falling back to default rules.")
            return self._default_standards()

    def _extract_rules_from_dir(self, directory: str) -> str:
        collected = []
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith((".md", ".txt")):
                    fp = os.path.join(root, file)
                    try:
                        with open(fp, "r", encoding="utf-8") as f:
                            collected.append(f"--- Standard File: {file} ---\n" + f.read()[:1500])
                    except Exception:
                        pass
        return "\n\n".join(collected) if collected else self._default_standards()

    def _default_standards(self) -> str:
        return """
Department Coding Standard: Financial Microservices QA Guidelines
1. Assertion Standards:
   - MUST use AssertJ `assertThat(...)` rather than legacy JUnit `assertEquals`.
   - Never write single `assertNotNull` without validating substantive state.
2. Structure & Readability:
   - Tests MUST follow BDD structure with clear Given, When, Then section comments.
   - Display names (@DisplayName) MUST be written in plain English describing behavior.
3. Resilience & Exception Testing:
   - Expected exceptions MUST be asserted using `assertThatThrownBy(...)`.
   - Any database modifying method with @Transactional MUST have rollback validation.
"""
