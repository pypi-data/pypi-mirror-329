import inspect
from typing import Dict, Any
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition

class ReadFileToolDefinition(ToolDefinition):
    name: str = "read_file"
    description: str = "Read a file from the file system."
    parameters: Dict[str, str] = {
        "path": "(required) The path of the file to read."
    }
    usage: str = inspect.cleandoc("""
    <read_file>
    <path>File path here</path>
    </read_file>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        with open(args["path"], "r") as f:
            content = f.read()
        return f"<file_content>\n{content}\n</file_content>" 