from typing import Optional, Dict, Any
from ..configs.settings import get_settings
from ..utils.logger import logger


class JiraClient:
    """Jira REST client for fetching acceptance criteria, with markdown fallback."""

    def __init__(self):
        self.settings = get_settings()

    def get_issue_acceptance_criteria(self, issue_id: Optional[str], repo_fallback_path: Optional[str] = None) -> str:
        if not issue_id:
            logger.info("No Jira issue specified; falling back to local documentation/README specs.")
            return self._extract_from_repo(repo_fallback_path)

        logger.info(f"Querying Jira issue {issue_id}...")
        # If credentials configured, use jira library; otherwise fallback
        if self.settings.JIRA_SERVER_URL and self.settings.JIRA_API_TOKEN:
            try:
                from jira import JIRA
                jira = JIRA(
                    server=self.settings.JIRA_SERVER_URL,
                    basic_auth=(self.settings.JIRA_USERNAME, self.settings.JIRA_API_TOKEN)
                )
                issue = jira.issue(issue_id)
                description = issue.fields.description or ""
                return description
            except Exception as e:
                logger.error(f"Failed to fetch Jira ticket {issue_id}: {e}; falling back to local docs.")

        return self._extract_from_repo(repo_fallback_path)

    def _extract_from_repo(self, repo_path: Optional[str]) -> str:
        if not repo_path:
            return "Default Enterprise Business Rules: Balance must not be negative, concurrency lock required."
        import os
        candidates = ["README.md", "docs/REQUIREMENTS.md", "docs/spec.md"]
        for cand in candidates:
            p = os.path.join(repo_path, cand)
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8") as f:
                    return f.read()[:2000]
        return "Standard Banking Rules: Safe transfer, transaction rollback, input validation."
