import inspect
from typing import Dict, Any
from stefan.utils.file_creator import FileCreator
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition
from stefan.utils.multiline import multiline

class CreateMultipleFilesToolDefinition(ToolDefinition):
    name: str = "create_multiple_files"
    description: str = "Create multiple new files with specified content."
    parameters: Dict[str, str] = {
        "file_contents": "(required) A dictionary mapping file paths to their content."
    }
    usage: str = inspect.cleandoc("""
    <create_multiple_files>
        <file>
            <path>path/to/file1</path>
            <content>content1</content>
        </file>
        <file>
            <path>path/to/file2</path>
            <content>content2</content>
        </file>
    </create_multiple_files>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        file_content_map = {file["path"]: file["content"] for file in args["file"]}
        return FileCreator.create_multiple_files(files_dict=file_content_map) 