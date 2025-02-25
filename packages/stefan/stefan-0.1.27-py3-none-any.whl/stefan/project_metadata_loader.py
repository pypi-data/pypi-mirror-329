import yaml
from pathlib import Path
from typing import Optional

from stefan.project_metadata import ProjectMetadata

class ProjectMetadataLoader:
    @staticmethod
    def load_from_file(file_path: Path) -> ProjectMetadata:
        """
        Load project metadata from a YAML file.
        
        Args:
            file_path: Path to the YAML metadata file
            
        Returns:
            ProjectMetadata object containing the loaded data
            
        Raises:
            FileNotFoundError: If the metadata file doesn't exist
            yaml.YAMLError: If the YAML file is invalid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {file_path}")
            
        with open(file_path, 'r') as f:
            data = yaml.safe_load(f)
            
        return ProjectMetadata(**data) 