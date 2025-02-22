import inspect
from typing import Dict, Any
from stefan.utils.file_creator import FileCreator
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition

class CreateFileToolDefinition(ToolDefinition):
    name: str = "create_file"
    description: str = "Create a new file with specified content."
    parameters: Dict[str, str] = {
        "file_path": "(required) The path of the file to create.",
        "content": "(required) The content to write to the file."
    }
    usage: str = inspect.cleandoc("""
    <create_file>
    <file_path>Your file path here</file_path>
    <content>Your file content here</content>
    </create_file>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        return FileCreator.create_file(file_path=args["file_path"], content=args["content"]) 