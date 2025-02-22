import inspect
from typing import Dict, Any
from stefan.execution_context import ExecutionContext
from stefan.utils.file_reader import FileReader
from stefan.tool.tool_definition import ToolDefinition
from stefan.utils.multiline import multiline

class ReadMultipleFilesToolDefinition(ToolDefinition):
    name: str = "read_multiple_files"
    description: str = "Read multiple files from the file system."
    parameters: Dict[str, str] = {
        "paths": "(required) A list of file paths to read."
    }
    usage: str = inspect.cleandoc("""
    <read_multiple_files>
        <path>path/to/file1</path>
        <path>path/to/file1</path>                               
    </read_multiple_files>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        return FileReader.read_multiple_files(args["path"]) 
