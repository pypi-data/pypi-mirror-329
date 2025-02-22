from typing import Dict, Optional
from pydantic import BaseModel

from stefan.execution_context import ExecutionContext

# Base class for tool definitions
class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: Dict[str, str]
    usage: str

    def get_extra_info(self, context: ExecutionContext) -> Optional[str]:
        """Optional method to provide additional dynamic information about the tool.
        Can be overridden by subclasses to add custom dynamic information.
        
        Returns:
            Optional[str]: Additional dynamic information or None if not implemented
        """
        return None
