from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import UUID
from enum import Enum
from pydantic import BaseModel, computed_field

#region EXECUTION NODE

class ExecutionNodeType(Enum):
    AGENT = "agent"
    TOOL = "tool"

class ExecutionParams(BaseModel):
    params: Any

class ExecutionError(BaseModel):
    message: str
    stacktrace: str

class TimeExecutionData(BaseModel):
    start_time: datetime
    end_time: Optional[datetime]
    
    @computed_field
    @property
    def duration_ms(self) -> Optional[float]:
        if self.end_time is None:
            return None
        return (self.end_time - self.start_time).total_seconds() * 1000
    
class BaseExecutionNode(BaseModel):
    id: UUID
    parent_agent_id: Optional[UUID]
    node_type: ExecutionNodeType
    name: str
    depth: int
    time_execution_data: TimeExecutionData

#endregion

#region LLM MESSAGES

class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

class LLMMessage(BaseModel):
    role: MessageRole
    content: str

#endregion

#region AGENTS DATA

class AgentExecutionStatus(Enum):
    STARTED = "started"
    CONTINUE = "continue"
    COMPLETED = "completed"
    FAILED = "failed"

class ModelConfigData(BaseModel):
    model_name: str
    temperature: float
    max_tokens: int

class TokenUsageData(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    cost: float

class AgentInputDataSource(Enum):
    AGENT_CREATED_BY_USER = "agent_created_by_user"
    AGENT_CREATED_BY_AGENT = "agent_created_by_agent"
    AGENT_RESULT = "agent_result"
    TOOL_RESULT = "tool_result"

class AgentInputData(BaseModel):
    params: ExecutionParams
    source: AgentInputDataSource

#endregion

#region AGENT OUTPUT

class AgentOutputAction(BaseModel):
    pass

class StartChildAgentAction(AgentOutputAction):
    child_agent_name: str
    params: ExecutionParams

class StartChildToolAction(AgentOutputAction):
    child_tool_name: str
    params: ExecutionParams

class FinishAgentAction(AgentOutputAction):
    params: ExecutionParams

class AgentExecutionNode(BaseExecutionNode):
    input_data: AgentInputData
    llm_messages: List[LLMMessage]
    execution_status: AgentExecutionStatus
    model_config_data: ModelConfigData

    # There properties are set when agent is finished
    llm_response: Optional[LLMMessage]
    token_usage: Optional[TokenUsageData]
    output_action: Optional[AgentOutputAction]
    output_error: Optional[ExecutionError]

#endregion

#region TOOLS DATA

class ToolExecutionStatus(Enum):
    RUNNING = "started"
    COMPLETED = "completed"
    FAILED = "failed"

class ToolExecutionNode(BaseExecutionNode):
    input_data: ExecutionParams
    execution_status: ToolExecutionStatus

    # These properties are set when tool is finished
    output_data: Optional[ExecutionParams] = None
    output_metadata: Optional[Dict[str, str]] = None
    output_error: Optional[ExecutionError] = None

#endregion