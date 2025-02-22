from typing import Dict, Any
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition
from stefan.utils.file_writer import FileWriter
from stefan.utils.multiline import multiline

class WriteMultipleFilesToolDefinition(ToolDefinition):
    name: str = "write_multiple_files"
    description: str = multiline("""
        Write content to multiple files at once.
        - should be used only with full content of files
        - do not provide partial content since it will replace the whole file
        - do not include any additional text, comments or instructions
        - content is automatically saved to the file and is not processed by another human
        Should be used when you need to write full content of the file with a lot of changes at multiple places (prefer text_replace tool for simple edits).
        """)
    parameters: Dict[str, str] = {
        "file_content_map": "(required) A dictionary mapping file paths to their content."
    }
    usage: str = multiline("""
        <write_multiple_files>
            <file>
                <path>path/to/file1</path>
                <content>content1</content>
            </file>
            <file>
                <path>path/to/file2</path>
                <content>content2</content>
            </file>
        </write_multiple_files>
        """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        file_content_map = {file["path"]: file["content"] for file in args["file"]}
        results = FileWriter.write_multiple_files(file_content_map)
        return '\n'.join(results) 