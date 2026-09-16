import os
from typing import Optional
import git
from ..utils.logger import logger


class GitClient:
    """Git repository management helper for cloning, branching, and creating commits."""

    @staticmethod
    def clone_repository(repo_url: str, local_path: str, branch: str = "main") -> git.Repo:
        logger.info(f"Cloning repository {repo_url} (branch: {branch}) into {local_path}")
        os.makedirs(local_path, exist_ok=True)
        return git.Repo.clone_from(repo_url, local_path, branch=branch)

    @staticmethod
    def create_and_checkout_branch(repo: git.Repo, branch_name: str) -> None:
        logger.info(f"Checking out new branch: {branch_name}")
        new_branch = repo.create_head(branch_name)
        new_branch.checkout()

    @staticmethod
    def commit_and_push(repo: git.Repo, commit_message: str, branch_name: str) -> None:
        logger.info(f"Committing changes: {commit_message}")
        repo.git.add(all=True)
        repo.index.commit(commit_message)
        logger.info(f"Pushing branch {branch_name} to origin")
        repo.remote(name="origin").push(refspec=f"{branch_name}:{branch_name}")
