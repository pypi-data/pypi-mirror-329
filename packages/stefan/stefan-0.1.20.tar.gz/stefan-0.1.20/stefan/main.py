#!/usr/bin/env python
import argparse
import json
import os
from pathlib import Path
import traceback
from datetime import datetime

from dotenv import load_dotenv

from stefan.agent.agent_executor_new import AgentExecutorNew
from stefan.agent.agent_planner import PlannerAgent
from stefan.code_search.llm.llm_logger import LLMLogger
from stefan.dependencies.service_locator import ServiceLocator
from stefan.execution_context import ExecutionContext
from stefan.execution_input_args import ExecutionInputArgs
from stefan.execution_tree.execution_tree_builder import ExecutionTreeBuilder
from stefan.project_configuration import STEFAN_CONFIG_DIRECTORY, STEFAN_OUTPUTS_DIRECTORY, ExecutionTreeSettings, ProjectContext
from stefan.project_metadata_loader import ProjectMetadataLoader
from stefan.utils.xml_answer_parser import XMLAnswerParser
from stefan.code_search.llm.llm_model import LLM_MODEL

load_dotenv()

def start_agent(project_context: ProjectContext):
    args = get_arguments()

    # Initialize agent executor with planner agent
    initial_agent = PlannerAgent.create_instance(allow_self_use=True)

    # Create project context
    context = ExecutionContext.initial(
        current_agent=initial_agent,
        project_context=project_context,
    )

    # Create agent executor
    agent_executor = AgentExecutorNew(
        agent=initial_agent, 
        service_locator=project_context.service_locator,
        main_agent_model=args.main_agent_model,
        child_agent_model=args.child_agent_model,
    )

    try:
        response = agent_executor.start_agent_by_user(user_request=args.task, context=context)
        if response.error is not None:
            raise response.error

        print("Process finished with success:\n\n")

        print(f"Answer raw:\n{response.result}\n\n")

        answer = XMLAnswerParser.parse_answer_xml(response.result)
        print("Answer formatted:\n" + json.dumps(answer.answer_dict, indent=2) + "\n\n")

    except Exception as e:
        print(f"Process failed with error:\n{e}\n\n")
        traceback.print_exc()

    print("")
    print("Stefan results:")
    print(f"- total cost: {project_context.service_locator.get_execution_tree_builder().get_total_cost()}")
    print(f"- total execution time: {project_context.service_locator.get_execution_tree_builder().get_total_execution_time()}")

def _setup_kotlin_project_and_create_project_context() -> ProjectContext:
    # Get command line arguments
    args = get_arguments()

    # Change working directory
    os.chdir(args.working_dir)

    # Let's create the service locator first
    service_locator = ServiceLocator()
    service_locator.initialize()

    # Initialize the project context
    project_context = _create_kotlin_project_context(args.working_dir, service_locator)
    
    # Initialize the service locator
    service_locator.set_llm_logger(LLMLogger(project_context))
    service_locator.set_execution_tree_builder(ExecutionTreeBuilder(project_context))

    return project_context

def _create_kotlin_project_context(working_dir: Path, service_locator: ServiceLocator):
    metadata_file_path = Path(working_dir) / STEFAN_CONFIG_DIRECTORY / "stefan_config.yaml"
    project_metadata = ProjectMetadataLoader().load_from_file(metadata_file_path)

    # Create absolute path for outputs
    outputs_dir = Path(working_dir) / STEFAN_OUTPUTS_DIRECTORY

    ProjectContext.model_rebuild()
    project_context = ProjectContext(
        execution_id=datetime.now().strftime('%Y%m%d_%H%M%S'),
        root_directory=Path(working_dir),
        execution_directory=outputs_dir,
        execution_tree_settings=ExecutionTreeSettings(save_on_update=True),
        service_locator=service_locator,
        metadata=project_metadata,
    )

    return project_context
    
def get_arguments():
    """
    Get command line arguments
    """ 
    parser = argparse.ArgumentParser(
        description='Run Stefan The Coder with a task description',
    )
    parser.add_argument(
        '--task',
        nargs='?',
        required=True,
        help='Description of the task to perform',
    )
    parser.add_argument(
        '--working-dir',
        default='.',
        help='Specify the working directory from which the script will be executed',
    )
    parser.add_argument(
        '--main-agent-model',
        default='CLAUDE_SONNET_3_5_NEW',
        choices=[model.name for model in LLM_MODEL],
        help='Model to use for the main agent',
    )
    parser.add_argument(
        '--child-agent-model',
        default='DEEPSEEK_R1',
        choices=[model.name for model in LLM_MODEL],
        help='Model to use for child agents',
    )
    parser.add_argument(
        '--allow-translation-updates',
        default=False,
        help="Allow translation updates. This will allow the agent to update the translation of the code in google sheets (risky and we don't have backup plan in case something went wrong)",
    )
    args = parser.parse_args()

    return ExecutionInputArgs(
        task=args.task,
        working_dir=Path(args.working_dir),
        main_agent_model=LLM_MODEL[args.main_agent_model],
        child_agent_model=LLM_MODEL[args.child_agent_model],
        allow_translation_updates=args.allow_translation_updates,
    )

def main():
    project_context = _setup_kotlin_project_and_create_project_context()
    start_agent(project_context=project_context)
    #script_show_directory(project_context=project_context)
    #script_sheet_happen_show_all()

if __name__ == "__main__":
    main()