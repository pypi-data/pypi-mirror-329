from pydantic import BaseModel

class PromptTemplate(BaseModel):
    agents_use_prompt: str
    tools_use_prompt: str
    file_paths_rules_prompt: str
    metadata_project_context_prompt: str
    answer_format_prompt: str
