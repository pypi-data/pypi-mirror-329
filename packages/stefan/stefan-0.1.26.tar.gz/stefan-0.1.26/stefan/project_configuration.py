from __future__ import annotations

from pathlib import Path
from typing import Any, List
from pydantic import BaseModel

from stefan.project_metadata import ProjectMetadata


class ExecutionTreeSettings(BaseModel):
    save_on_update: bool

class ProjectContext(BaseModel):    
    execution_id: str
    root_directory: Path
    execution_directory: Path
    execution_tree_settings: ExecutionTreeSettings
    service_locator: Any
    metadata: ProjectMetadata
    

    @property
    def exclude_patterns(self) -> List[str]:
        return self.metadata.exclude_patterns

    @property
    def include_patterns(self) -> List[str]:
        return self.metadata.include_patterns
    
STEFAN_CONFIG_DIRECTORY = "stefan_config"
STEFAN_OUTPUTS_DIRECTORY = ".stefan_output"
