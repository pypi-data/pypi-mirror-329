from __future__ import annotations

from typing import Any
from pydantic import BaseModel

class ExecutionContext(BaseModel):
    current_tool: Any | None = None     # Should be always be a ToolDefinition but we want to avoid circular import
    current_agent: Any | None = None    # Should be always be an AgentDefinition but we want to avoid circular import
    parent_agent: Any | None = None     # Should be always be an AgentDefinition but we want to avoid circular import
    project_context: Any | None = None  # Should be always be a ProjectContext but we want to avoid circular import
    depth: int = 0

    @classmethod
    def empty(cls) -> 'ExecutionContext':
        return ExecutionContext()
    
    @classmethod
    def test(cls, project_context: 'ProjectContext') -> 'ExecutionContext':
        return ExecutionContext(project_context=project_context)
    
    @classmethod
    def initial(cls, current_agent: Any, project_context: 'ProjectContext') -> 'ExecutionContext':
        return ExecutionContext(current_agent=current_agent, project_context=project_context)
    
    def copy(
        self,
        current_tool: Any | None = None,
        current_agent: Any | None = None,
        parent_agent: Any | None = None,
        depth: int | None = None,
    ) -> 'ExecutionContext':
        return ExecutionContext(
            current_tool=current_tool or self.current_tool,
            current_agent=current_agent or self.current_agent,
            parent_agent=parent_agent or self.parent_agent,
            project_context=self.project_context,
            depth=depth or self.depth,
        )
