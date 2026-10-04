import os
import re
from pathlib import Path

from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai.tasks.task_output import TaskOutput
from crewai_tools import FileReadTool, FileWriterTool

from coding_agent.tools.run_tests_tool import RunTestsTool


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "output"
_PYTHON_FENCE = re.compile(r"```(?:python)?\s*\n(.*?)```", re.DOTALL)


def _extract_python_source(text: str) -> str | None:
    fenced = _PYTHON_FENCE.findall(text)
    if fenced:
        return max(fenced, key=len).strip() + "\n"
    stripped = text.strip()
    if stripped.startswith(("import ", "from ", "def ", "class ", '"""', "'''")):
        return stripped + "\n"
    return None


def _ensure_app_py(output: TaskOutput) -> None:
    """Save app.py from the developer answer when the file tool was not used."""
    app_path = OUTPUT_DIR / "app.py"
    if app_path.is_file() and app_path.stat().st_size > 0:
        return
    code = _extract_python_source(output.raw or "")
    if not code:
        return
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    app_path.write_text(code, encoding="utf-8")


@CrewBase
class CodingAgent():
    """CodingAgent crew"""

    agents: list[BaseAgent]
    tasks: list[Task]

    @agent
    def business_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config['business_analyst'], # type: ignore[index]
            verbose=True
        )

    @agent
    def developer(self) -> Agent:
        return Agent(
            config=self.agents_config['developer'], # type: ignore[index]
            verbose=True,
            tools=[FileWriterTool(base_dir=str(OUTPUT_DIR))],
        )

    @agent
    def tester(self) -> Agent:
        return Agent(
            config=self.agents_config['tester'], # type: ignore[index]
            verbose=True,
            tools=[
                FileReadTool(base_dir=str(OUTPUT_DIR)),
                FileWriterTool(base_dir=str(OUTPUT_DIR)),
                RunTestsTool(output_dir=str(OUTPUT_DIR)),
            ],
        )

    @task
    def business_analyst_task(self) -> Task:
        return Task(
            config=self.tasks_config['business_analyst_task'], # type: ignore[index]
            output_file='output/spec.md',
            create_directory=True,
        )

    @task
    def developer_task(self) -> Task:
        return Task(
            config=self.tasks_config['developer_task'], # type: ignore[index]
            callback=_ensure_app_py,
        )

    @task
    def tester_task(self) -> Task:
        return Task(
            config=self.tasks_config['tester_task'], # type: ignore[index]
            output_file='output/test_report.md',
            create_directory=True,
        )

    @crew
    def crew(self) -> Crew:
        """Creates the CodingAgent crew"""
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        os.chdir(PROJECT_ROOT)
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
