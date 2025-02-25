import re
from typing import Any, Dict
from pydantic import BaseModel

from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition

class ToolResult(BaseModel):
    was_used: bool
    result: str | None = None
    error: Exception | None = None

    class Config:
        arbitrary_types_allowed = True # Allow error to be an Exception

    @classmethod
    def create_used(cls, result: str) -> "ToolResult":
        return cls(was_used=True, result=result)

    @classmethod
    def create_not_used(cls) -> "ToolResult":
        return cls(was_used=False)
    
    @classmethod
    def create_used_with_error(cls, error: Exception) -> "ToolResult":
        return cls(was_used=True, error=error)

class ToolExecutor:

    def __init__(self, tool: ToolDefinition):
        self.tool = tool

    def parse_and_execute(self, input_string: str, context: ExecutionContext) -> ToolResult:
        """
        Detects if the tool is mentioned in the input string, parses arguments, and executes the tool.
        
        Args:
            input_string (str): The input string containing tool usage.
        
        Returns:
            str: The result of the tool execution.
        """
        if f"<{self.tool.name}>" in input_string:
            tool_executor = ToolExecutor(self.tool)
            args = tool_executor.parse_arguments(input_string)
            new_context = context.copy(current_tool=self.tool)
            try:
                result = self.tool.execute_tool(args, new_context)
                return ToolResult.create_used(result)
            except Exception as error:
                return ToolResult.create_used_with_error(error)
        
        return ToolResult.create_not_used()
    
    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> ToolResult:
        new_context = context.copy(current_tool=self.tool)
        try:
            result = self.tool.execute_tool(args, new_context)
            return ToolResult.create_used(result)
        except Exception as error:
            return ToolResult.create_used_with_error(error)

    def parse_arguments(self, input_string: str) -> Dict[str, Any]:
        """
        Parses arguments from the input string based on the tool's parameters.
        
        Args:
            input_string (str): The input string containing tool usage.
        
        Returns:
            Dict[str, Any]: Parsed arguments.
        """
        args = {}
        for param in self.tool.parameters.keys():
            match = re.search(f"<{param}>(.*?)</{param}>", input_string, re.DOTALL)
            if match:
                args[param] = match.group(1)
        return args
