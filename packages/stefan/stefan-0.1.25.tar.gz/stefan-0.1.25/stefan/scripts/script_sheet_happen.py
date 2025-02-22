from stefan.execution_context import ExecutionContext
from stefan.tool.tool_localization import LocalizationToolDefinition

def script_sheet_happen_show_all():
    print(LocalizationToolDefinition().execute_tool(args={}, context=ExecutionContext.test()))
