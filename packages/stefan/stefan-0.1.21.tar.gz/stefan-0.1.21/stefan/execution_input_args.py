from pathlib import Path

from pydantic import BaseModel

from stefan.code_search.llm.llm_model import LLM_MODEL

class ExecutionInputArgs(BaseModel):
    task: str
    working_dir: Path
    main_agent_model: LLM_MODEL
    child_agent_model: LLM_MODEL
    allow_translation_updates: bool = False
