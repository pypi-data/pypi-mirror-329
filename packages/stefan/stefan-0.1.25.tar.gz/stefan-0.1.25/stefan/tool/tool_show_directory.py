import inspect
from typing import Dict, Any
from stefan.utils.directory_tree_visualizer import DirectoryTreeVisualizer
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition
from stefan.utils.multiline import multiline

class ShowDirectoryToolDefinition(ToolDefinition):
    name: str = "show_directory"

    description: str = "Recursively shows all files with given postfix in directory."
    
    parameters: Dict[str, str] = {
        "directory": "(required) Path to the directory to list.",
        "postfix": "(optional) File extension filter (e.g., '*.py')."
    }
    
    usage: str = multiline("""
        <show_directory>
            <directory>...</directory>
            <postfix>...</postfix>
        </show_directory>
        """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        return DirectoryTreeVisualizer.show_directory(
            directory=args["directory"],
            project_context=context.project_context,
            postfix=args.get("postfix"), # Optional parameter
        )
