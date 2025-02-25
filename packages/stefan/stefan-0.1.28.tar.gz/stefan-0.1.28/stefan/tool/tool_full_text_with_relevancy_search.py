import inspect
from typing import Any, Dict
from stefan.dependencies.service_locator import ServiceLocator
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition

class FullTextWithRelevancySearchToolDefinition(ToolDefinition):
    name: str = "full_text_with_relevancy_search"
    description: str = inspect.cleandoc("""
    Searches for files in the current directory using the following algorithm:
    1) first, a full text search (case sensitive)
    2) then it will go over the results and use a LLM to filter out the relevant files
    Should be used when you want to search for example for usage of a specific function and want to filter out the irrelevant files.
    This may be helpful when you want to search for example for usage of 'get_user' function which is implemented multiple times but in different contexts.
    """)
    parameters: Dict[str, str] = {
        "full_text_query": "(required) The query to search for. The algorithm will select files only with exact matches.",
        "llm_query": "(required) The query to use as a relevance filter. Should be a detailed question that can be answered by the file content.",
    }
    usage: str = inspect.cleandoc("""
    <full_text_with_relevancy_search>
    <full_text_query>Directory path here</full_text_query>
    <llm_query>Detailed question that can be answered by the file content.</llm_query>
    </full_text_with_relevancy_search>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        full_text_search = ServiceLocator().create_full_text_search(project_context=context.project_context)

        files = full_text_search.perform_search_fulltext(
            fulltext_search_query=args["query"],
            context=context,
        )

        return "\n".join([f"File: {file.file_path}\nRelevance score: {file.relevance_score}\nExplanation: {file.explanation}" for file in files])
