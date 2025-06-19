from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List


@CrewBase
class DdtAwsAdf:
    """DdtAwsAdf crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    @agent
    def discovery_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["discovery_engineer"],  # type: ignore[index]
            verbose=False,
        )

    @agent
    def mapping_analyst(self) -> Agent:
        return Agent(
            config=self.agents_config["mapping_analyst"],  # type: ignore[index]
            verbose=False,
        )

    @agent
    def notebook_engineer(self) -> Agent:
        return Agent(
            config=self.agents_config["notebook_engineer"],  # type: ignore[index]
            verbose=False,
        )

    @task
    def discovery_task(self) -> Task:
        return Task(
            config=self.tasks_config["discovery_task"],  # type: ignore[index]
        )

    @task
    def mapping_task(self) -> Task:
        return Task(
            config=self.tasks_config["mapping_task"],  # type: ignore[index]
            output_file="mapping_report.md",
        )

    @task
    def notebook_task(self) -> Task:
        return Task(
            config=self.tasks_config["notebook_task"],  # type: ignore[index]
            output_file="databricks_notebook.py",
        )

    @crew
    def crew(self) -> Crew:
        """Creates the DdtAwsAdf crew"""

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=False,
        )
