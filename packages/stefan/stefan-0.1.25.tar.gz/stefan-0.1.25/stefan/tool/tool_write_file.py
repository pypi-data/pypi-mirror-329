import inspect
from typing import Dict, Any
from stefan.utils.file_writer import FileWriter
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition
from stefan.utils.multiline import multiline

class WriteFileToolDefinition(ToolDefinition):
    name: str = "write_to_file"
    description: str = multiline("""
        Write content to an existing file.
        - should be used only with full content of the file
        - do not provide partial content since it will replace the whole file
        - do not include any additional text, comments or instructions
        - content is automatically saved to the file and is not processed by another human                        
        Should be used when you need to write full content of the file with a lot of changes at multiple places (prefer text_replace tool for simple edits).
        """)
    parameters: Dict[str, str] = {
        "file_path": "(required) The path of the file to write to.",
        "content": "(required) The content to write to the file. Always provide full content, do not provide partial content. Do not include any additional text, comments or instructions.",
        "mode": "(optional) Write mode: 'w' for overwrite, 'a' for append."
    }
    usage: str = multiline("""
        <write_to_file>
            <file_path>Your file path here</file_path>
            <content>Your file content here</content>
            <mode>w</mode>
        </write_to_file>
        """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        return FileWriter.write_file(
            file_path=args["file_path"],
            content=args["content"],
            mode=args.get("mode", "w")  # Optional parameter with default
        ) 