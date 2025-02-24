import inspect
from typing import Dict, Any, Optional

from overrides import override
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition
from stefan.utils.command_executor import CommandExecutor

class ExecuteCommandToolDefinition(ToolDefinition):
    name: str = "execute_command"
    description: str = "Execute one of available CLI commands and return the stdout or stderr."
    parameters: Dict[str, str] = {
        "command": "The command to execute"
    }
    usage: str = inspect.cleandoc("""
        <execute_command>
            <command>executable command</command>
        </execute_command>
        """)

    @override
    def get_extra_info(self, context: ExecutionContext) -> Optional[str]:
        available_commands = context.project_context.metadata.available_commands

        extra_info = "\nAvailable commands (you should use only the following commands. Any other command will be rejected!!!):"
        extra_info += "\n".join([f"\nCommand: {command.command}\nDescription: {command.description}" for command in available_commands])

        return extra_info

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        available_commands = {command.command for command in context.project_context.metadata.available_commands}
        command_to_execute = args["command"].strip()

        if command_to_execute not in available_commands:
            return f"Command not found in available commands.\nCommand: {command_to_execute}\nAvailable commands: {available_commands}"

        _, message = CommandExecutor().execute(command_to_execute)
        return message
