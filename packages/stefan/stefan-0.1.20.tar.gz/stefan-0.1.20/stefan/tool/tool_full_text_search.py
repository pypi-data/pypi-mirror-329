import inspect
from typing import Any, Dict
from stefan.dependencies.service_locator import ServiceLocator
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition

class FullTextSearchToolDefinition(ToolDefinition):
    name: str = "full_text_search"
    description: str = "Searches for files in the current directory using full text search (case sensitive)."
    parameters: Dict[str, str] = {
        "query": "(required) The query to search for. The algorithm will select files only with exact matches.",
    }
    usage: str = inspect.cleandoc("""
    <full_text_search>
    <query>Directory path here</query>
    </full_text_search>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        full_text_search = context.project_context.service_locator.create_full_text_search(project_context=context.project_context)

        files = full_text_search.perform_search_fulltext(
            fulltext_search_query=args["query"],
            context=context,
        )

        return "\n".join([f"File: {file.file_path}" for file in files])
