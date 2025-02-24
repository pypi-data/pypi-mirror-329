from __future__ import annotations
from pydantic import BaseModel
from typing import Dict, List

from stefan.agent.prompt_template import PromptTemplate
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.tool.tool_definition import ToolDefinition

class AgentDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, str]
    llm_tag: LLMTag
    usage: str
    available_agents: List['AgentDefinition']
    available_tools: List[ToolDefinition]

    def create_system_prompt(self, prompt_template: PromptTemplate, context: ExecutionContext) -> str:
        """
        Creates the system prompt for the agent.
        This method should be implemented by subclasses.
        
        Returns:
            str: The system prompt for the agent.
        """
        raise NotImplementedError("Subclasses must implement _create_system_prompt()")
        