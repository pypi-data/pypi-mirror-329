import os
from pathlib import Path
from stefan.execution_context import ExecutionContext
from stefan.project_configuration import STEFAN_CONFIG_DIRECTORY
from stefan.utils.multiline import multiline

def create_metadata_project_context_prompt(context: ExecutionContext) -> str:
    md_files_content = _load_md_files_from_directory(STEFAN_CONFIG_DIRECTORY)
    
    return _PROJECT_CONTEXT_PROMPT.format(
        project_context=context.project_context.metadata.project_context,
        md_files=md_files_content
    )

def _load_md_files_from_directory(directory: str) -> str:
    """Load and concatenate all .md files from the specified directory."""
    md_content = []
    
    try:
        for file in Path(directory).glob("*.md"):
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                if content:
                    md_content.append(f"# {file.name}\n{content}")
    except Exception as e:
        print(f"Error loading MD files: {e}")
        return ""
    
    return "\n\n".join(md_content)

_PROJECT_CONTEXT_PROMPT = """
# USER PROVIDED PROJECT CONTEXT
                     
The following section provides the user provided project context. These informations may be useful for you but be careful with them and use them more as a reference than a strict rule.
                
{md_files}
"""
