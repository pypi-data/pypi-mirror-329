from typing import List
from pydantic import BaseModel

class MainContext(BaseModel):
    """Information about project context and structure documentation.

    Attributes:
        path: Path to the context documentation file
        description: Brief description of what the context document contains
    """
    path: str
    description: str

class ExternalReference(BaseModel):
    """External reference or documentation used in the project.

    Attributes:
        path: URL or path to the external reference
        description: Description of what this reference contains or is used for
    """
    path: str
    description: str

class AvailableCommand(BaseModel):
    """Command that can be executed in the project.

    Attributes:
        command: The actual command to execute
        description: Description of what the command does
    """
    command: str
    description: str

class ModuleDescription(BaseModel):
    """Description of a project module and its structure.

    Attributes:
        module_name: Name of the module
        module_root_path: Root directory path of the module
        module_source_path: Path to the module's source code
        module_description: Detailed description of the module's purpose and contents
    """
    module_name: str
    module_root_path: str
    module_source_path: str
    module_description: str

class CodeSampleFile(BaseModel):
    """Reference to a specific code sample file.

    Attributes:
        path: Path to the code sample file
        description: Description of what the code sample demonstrates
    """
    path: str
    description: str

class CodeSample(BaseModel):
    """Collection of related code samples with documentation.

    Attributes:
        description: Overview of what these code samples demonstrate
        tutorial: Path to the tutorial document explaining the code samples
        files: List of code sample files and their descriptions
    """
    description: str
    tutorial_path: str
    example_files: List[CodeSampleFile] = []

class LocalizationSheet(BaseModel):
    sheet_url: str

class ProjectMetadata(BaseModel):
    """Complete metadata structure for the project.

    Contains all project-related information including documentation,
    module structure, available commands, and code samples.

    Attributes:
        project_context: List of project context documentation
        external_references: List of external documentation and references
        available_commands: List of executable project commands
        modules_description: List of module descriptions and their structure
        code_samples: List of code samples with their documentation
    """
    include_patterns: List[str] = []
    exclude_patterns: List[str] = []
    project_context: List[MainContext] = []
    external_references: List[ExternalReference] = []
    available_commands: List[AvailableCommand] = []
    modules_description: List[ModuleDescription] = []
    code_samples: List[CodeSample] = []
    local_translations_xml_file: str | None = None
    localization_sheet: LocalizationSheet | None = None
