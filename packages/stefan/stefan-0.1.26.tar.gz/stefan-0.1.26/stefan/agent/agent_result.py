from __future__ import annotations
from pydantic import BaseModel

class AgentResult(BaseModel):
    result: str | None = None
    error_message: str | None = None
    error: Exception | None = None

    class Config:
        arbitrary_types_allowed = True # Allow error to be an Exception

    @classmethod
    def create_success(cls, result: str) -> "AgentResult":
        return cls(result=result, error_message=None, error=None)

    @classmethod
    def create_failure(cls, error_message: str, error: Exception) -> "AgentResult":
        return cls(result=None, error_message=error_message, error=error)
