from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition

class ToolFormatter:
    def format_tool(self, tool: ToolDefinition, context: ExecutionContext) -> str:
        """
        Formats the tool information for display.
        
        Returns:
            str: Formatted tool information.
        """
        params = "\n".join([f"- {key}: {value}" for key, value in tool.parameters.items()])
        base_info = f"## {tool.name}\nDescription: {tool.description}\nParameters:\n{params}\nUsage:\n{tool.usage}"

        # Add extra information if available
        dynamic_info = tool.get_extra_info(context)
        if dynamic_info:
            base_info += f"\n\n{dynamic_info}"
        base_info += "\n\n"
            
        return base_info
