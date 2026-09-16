import subprocess
import os
from typing import Dict, Any
from ..utils.logger import logger


class MavenSandbox:
    """Subprocess runner for isolated Maven test execution."""

    @staticmethod
    def run_tests(project_dir: str, timeout: int = 180) -> Dict[str, Any]:
        logger.info(f"Running `mvn clean test` in {project_dir}...")
        pom_path = os.path.join(project_dir, "pom.xml")
        if not os.path.exists(pom_path):
            return {
                "success": False,
                "exit_code": -1,
                "stdout": "pom.xml not found in target repository",
                "stderr": ""
            }

        try:
            res = subprocess.run(
                ["mvn", "test", "-Dtest=*Test"],
                cwd=project_dir,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            success = (res.returncode == 0)
            return {
                "success": success,
                "exit_code": res.returncode,
                "stdout": res.stdout,
                "stderr": res.stderr
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "exit_code": 124,
                "stdout": "Maven test execution timed out",
                "stderr": ""
            }
        except Exception as e:
            return {
                "success": False,
                "exit_code": 1,
                "stdout": str(e),
                "stderr": ""
            }
