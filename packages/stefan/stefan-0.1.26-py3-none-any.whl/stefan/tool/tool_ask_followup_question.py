import inspect
from typing import Dict, Any
from stefan.execution_context import ExecutionContext
from stefan.tool.tool_definition import ToolDefinition

class AskFollowupQuestionToolDefinition(ToolDefinition):
    name: str = "ask_followup_question"
    description: str = "Ask the user a question to gather additional information needed to complete the task."
    parameters: Dict[str, str] = {
        "question": "(required) The question to ask the user. This should be a clear, specific question that addresses the information you need."
    }
    usage: str = inspect.cleandoc("""
    <ask_followup_question>
    <question>Your question here</question>
    </ask_followup_question>
    """)

    def execute_tool(self, args: Dict[str, Any], context: ExecutionContext) -> str:
        print(f"Asking the user: {args['question']}")
        return input(f"Press Enter to continue...") 