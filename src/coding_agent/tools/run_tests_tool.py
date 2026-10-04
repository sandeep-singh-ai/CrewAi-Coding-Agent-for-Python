import re
import subprocess
import sys
from pathlib import Path

from crewai.tools import BaseTool
from pydantic import BaseModel, Field


class RunTestsInput(BaseModel):
    """Input for running unittest against one file in the output directory."""

    test_filename: str = Field(
        ...,
        description="Test module file name inside the output directory, for example test_app.py.",
    )


class RunTestsTool(BaseTool):
    """Run unittest for a test file saved in the crew output directory."""

    name: str = "Run Python Tests"
    description: str = (
        "Run Python's unittest on a test file that already exists in the output "
        "directory. Pass test_filename, for example test_app.py. The test module "
        "must import the application as app. Returns the test runner output and "
        "exit code. Does not modify files."
    )
    args_schema: type[BaseModel] = RunTestsInput
    output_dir: str

    def _run(self, test_filename: str) -> str:
        output_dir = Path(self.output_dir).resolve()
        filename = test_filename.strip()
        if not re.fullmatch(r"test_[A-Za-z0-9_]+\.py", filename):
            return (
                "Error: test_filename must be a file name like test_app.py "
                "with no directories."
            )

        test_path = (output_dir / filename).resolve()
        if not test_path.is_relative_to(output_dir):
            return "Error: the test file must stay inside the output directory."
        if not test_path.is_file():
            return (
                f"Error: {filename} is not in the output directory. "
                "Write it with the File Writer Tool before running tests."
            )

        try:
            completed = subprocess.run(
                [sys.executable, "-m", "unittest", filename[:-3], "-v"],
                cwd=output_dir,
                capture_output=True,
                text=True,
                timeout=60,
                check=False,
            )
        except subprocess.TimeoutExpired as exc:
            stdout = exc.stdout or ""
            stderr = exc.stderr or ""
            if isinstance(stdout, bytes):
                stdout = stdout.decode("utf-8", errors="replace")
            if isinstance(stderr, bytes):
                stderr = stderr.decode("utf-8", errors="replace")
            return _format_result(
                exit_code=124,
                stdout=stdout,
                stderr=stderr + "\nTests timed out after 60 seconds.",
            )

        return _format_result(
            exit_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )


def _format_result(exit_code: int, stdout: str, stderr: str) -> str:
    status = "passed" if exit_code == 0 else "failed"
    return (
        f"status: {status}\n"
        f"exit_code: {exit_code}\n"
        f"stdout:\n{_clip(stdout)}\n"
        f"stderr:\n{_clip(stderr)}"
    )


def _clip(text: str, limit: int = 12000) -> str:
    if len(text) <= limit:
        return text
    return text[-limit:]
