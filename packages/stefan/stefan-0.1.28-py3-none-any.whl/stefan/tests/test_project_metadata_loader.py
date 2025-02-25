import pytest
from pathlib import Path
import yaml

from stefan.project_metadata_loader import ProjectMetadataLoader
from stefan.project_metadata import ProjectMetadata
from stefan.utils.multiline import multiline

def test_load_metadata_from_file(tmp_path):
    yaml_content = multiline("""
      project_context:
        - path: docs/context.md
          description: Project overview

      external_references:
        - path: https://docs.example.com
          description: External API documentation

      available_commands:
        - command: test_command
          description: A test command

      modules_description:
        - module_name: test_module
          module_root_path: src/test_module
          module_source_path: src/test_module/core
          module_description: A test module

      code_samples:
        - description: Sample code
          tutorial_path: docs/tutorial.md
          example_files:
            - path: examples/file1.py
              description: First example
            - path: examples/file2.py
              description: Second example
      """)
    metadata_file = tmp_path / "test_metadata.yaml"
    metadata_file.write_text(yaml_content)
    
    # Load metadata from the test file
    metadata = ProjectMetadataLoader.load_from_file(metadata_file)
    
    # Verify the loaded metadata
    assert isinstance(metadata, ProjectMetadata)
    
    # Check project context
    assert len(metadata.project_context) == 1
    assert metadata.project_context[0].path == 'docs/context.md'
    assert metadata.project_context[0].description == 'Project overview'
    
    # Check external references
    assert len(metadata.external_references) == 1
    assert metadata.external_references[0].path == 'https://docs.example.com'
    assert metadata.external_references[0].description == 'External API documentation'
    
    # Check available commands
    assert len(metadata.available_commands) == 1
    assert metadata.available_commands[0].command == 'test_command'
    assert metadata.available_commands[0].description == 'A test command'
    
    # Check modules description
    assert len(metadata.modules_description) == 1
    assert metadata.modules_description[0].module_name == 'test_module'
    assert metadata.modules_description[0].module_root_path == 'src/test_module'
    assert metadata.modules_description[0].module_source_path == 'src/test_module/core'
    assert metadata.modules_description[0].module_description == 'A test module'
    
    # Check code samples
    assert len(metadata.code_samples) == 1
    assert metadata.code_samples[0].description == 'Sample code'
    assert metadata.code_samples[0].tutorial_path == 'docs/tutorial.md'
    assert len(metadata.code_samples[0].example_files) == 2
    assert metadata.code_samples[0].example_files[0].path == 'examples/file1.py'
    assert metadata.code_samples[0].example_files[0].description == 'First example'

def test_load_metadata_file_not_found():
    with pytest.raises(FileNotFoundError):
        ProjectMetadataLoader.load_from_file(Path('non_existent_file.yaml'))

def test_load_empty_metadata_file(tmp_path):
    yaml_content = "{}"
    empty_file = tmp_path / "empty_metadata.yaml"
    empty_file.write_text(yaml_content)
    
    metadata = ProjectMetadataLoader.load_from_file(empty_file)
    
    assert isinstance(metadata, ProjectMetadata)
    assert len(metadata.project_context) == 0
    assert len(metadata.external_references) == 0
    assert len(metadata.available_commands) == 0
    assert len(metadata.modules_description) == 0
    assert len(metadata.code_samples) == 0
