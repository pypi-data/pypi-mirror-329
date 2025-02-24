from typing import List
from stefan.code_search.llm.llm_logger import LLMLogger
from stefan.execution_context import ExecutionContext
from stefan.project_configuration import STEFAN_OUTPUTS_DIRECTORY, ExecutionTreeSettings, ProjectContext
from stefan.project_metadata import ProjectMetadata
from stefan.dependencies.service_locator import ServiceLocator
from pathlib import Path

def create_dummy_project_context(path: str = "", exclude_patterns: List[str] = [], include_patterns: List[str] = []) -> ProjectContext:
    project_metadata = ProjectMetadata(
        available_commands=[],
        modules_description=[],
        code_samples=[],
        exclude_patterns=exclude_patterns,
        include_patterns=include_patterns,
    )

    service_locator = ServiceLocator()
    service_locator.initialize()

    root_path = Path(path)
    project_context = ProjectContext(
        execution_id="123test123",
        root_directory=root_path,
        execution_directory=root_path / STEFAN_OUTPUTS_DIRECTORY,
        execution_tree_settings=ExecutionTreeSettings(save_on_update=False),
        service_locator=service_locator,
        metadata=project_metadata,
    )

    service_locator.set_llm_logger(LLMLogger(project_context, ignore_everything=True))

    return project_context

def create_execution_context_for_test(project_context: ProjectContext) -> ExecutionContext:
    return ExecutionContext.initial(current_agent=None, project_context=project_context)