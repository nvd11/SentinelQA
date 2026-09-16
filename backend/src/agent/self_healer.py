import os
from typing import Tuple
from langchain_core.messages import SystemMessage, HumanMessage

from ..llm.client import get_llm_model
from ..llm.prompts import SELF_HEALING_SYSTEM_PROMPT
from ..engine.maven_sandbox import MavenSandbox
from ..utils.logger import logger


class SelfHealer:
    """Reflects on Maven test execution failures and iteratively patches the generated tests."""

    def __init__(self, max_iterations: int = 3):
        self.llm = get_llm_model()
        self.max_iterations = max_iterations

    async def heal_until_green(
        self,
        project_dir: str,
        test_file_path: str,
        initial_test_code: str
    ) -> Tuple[bool, str, str]:
        logger.info(f"Starting self-healing loop for {test_file_path} (max: {self.max_iterations} iterations)...")

        current_code = initial_test_code
        # Write test code to target file
        with open(test_file_path, "w", encoding="utf-8") as f:
            f.write(current_code)

        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"--- Self-Healing Iteration {iteration}/{self.max_iterations} ---")
            sandbox_result = MavenSandbox.run_tests(project_dir)

            if sandbox_result["success"]:
                logger.info(f"Maven tests PASSED on iteration {iteration}!")
                return True, current_code, sandbox_result["stdout"]

            logger.warning(f"Maven build failed on iteration {iteration}. Initiating reflection...")
            error_log = sandbox_result["stdout"][-3000:] + "\n" + sandbox_result["stderr"][-1000:]

            prompt = f"""
TEST CODE:
{current_code}

MAVEN ERROR LOG:
{error_log}

Analyze why the test failed (compilation error, incorrect mock, assertion mismatch).
Patch the test code to fix the issue. Return ONLY the repaired Java code wrapped in ```java ... ```.
"""
            try:
                response = await self.llm.ainvoke([
                    SystemMessage(content=SELF_HEALING_SYSTEM_PROMPT),
                    HumanMessage(content=prompt)
                ])
                patched = response.content
                if "```java" in patched:
                    current_code = patched.split("```java")[1].split("```")[0].strip()
                elif "```" in patched:
                    current_code = patched.split("```")[1].split("```")[0].strip()

                with open(test_file_path, "w", encoding="utf-8") as f:
                    f.write(current_code)
            except Exception as e:
                logger.error(f"Failed during self-healing LLM reflection: {e}")
                break

        return False, current_code, "Self-healing exceeded max iterations without achieving green build."
