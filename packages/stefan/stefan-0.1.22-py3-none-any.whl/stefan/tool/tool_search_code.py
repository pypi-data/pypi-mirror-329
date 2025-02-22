import inspect
from typing import Any, Dict
from stefan.dependencies.service_locator import ServiceLocator
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition

class SearchCodeToolDefinition(ToolDefinition):
    name: str = "search_code_with_llm"
    description: str = "Searches for code in the current directory using a LLM as as relevance filter."
    parameters: Dict[str, str] = {
        "query": "(required) The query to search for. Since this is a LLM based search, the query should contain the detailed information to search for.",
    }
    usage: str = inspect.cleandoc("""
    <search_code_with_llm>
    <query>Directory path here</query>
    </search_code_with_llm>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        code_search = ServiceLocator().create_code_search(project_context=context.project_context)

        relevant_files = code_search.perform_search_with_query(
            query=args["query"],
            context=context,
            max_files=50,
            select_all_high_relevant_files=True,
        )

        return "\n".join([f"File: {file.file_path}\nDescription: {file.file_description}\nPublic Interface: {file.file_public_interface}\nRelevance Score: {file.relevance_score}\nExplanation: {file.explanation}" for file in relevant_files])