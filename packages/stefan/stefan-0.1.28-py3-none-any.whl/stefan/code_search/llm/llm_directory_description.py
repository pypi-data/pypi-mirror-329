import inspect

from pydantic import BaseModel
from stefan.code_search.file_system_nodes import DirectoryNode
from stefan.code_search.llm.llm_executor import LLMExecutor
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_model import LLM_MODEL
import re

from stefan.code_search.llm.llm_tag import LLMTag

class DirectoryDescriptionResult(BaseModel):
    description: str

class DirectoryDescriptionLLMProcessor:
    def __init__(self, llm_executor: LLMExecutor):
        self.llm_executor = llm_executor

    def extract_directory_description(self, directory_node: DirectoryNode) -> DirectoryDescriptionResult:
        """
        Extract directory description including descriptions of all direct children (files and subdirectories).
        Raises ValueError if any child description is missing.
        """
        # Get all direct children descriptions
        child_descriptions = []
        for child in directory_node.children:
            if child.description is None:
                raise ValueError(f"Missing description for {child.path}")
            child_descriptions.append(f"File {child.name}:\n{child.description}\n")
        child_descriptions_str = "\n".join(child_descriptions)

        # Get all subdirectories descriptions
        subdirectory_descriptions = []
        for subdir in directory_node.directories:
            if subdir.description is None:
                raise ValueError(f"Missing description for {subdir.path}")
            subdirectory_descriptions.append(f"Directory {subdir.name}:\n{subdir.description}\n")
        subdirectory_descriptions_str = "\n".join(subdirectory_descriptions)

        messages = [
            {
                "role": "system",
                "content": _SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": inspect.cleandoc(f"""
                    Analyze this directory structure and its contents:
                    
                    Current directory:
                                            
                    {directory_node.path}

                    Subdirectories:

                    {subdirectory_descriptions_str}
                    
                    Files:

                    {child_descriptions_str}
                """)
            }
        ]

        success_result, error = self.llm_executor.generate(
            tag=LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION,
            model=LLM_MODEL.OPEN_AI_4o_MINI,
            messages=messages,
            execution_context=ExecutionContext.empty(),
        ).unpack()

        # If there was an error, raise it - we don't want to skip this error
        if error is not None:
            raise error
        
        # Get response from LLM
        response = success_result.response

        # Extract description using regex
        description_match = re.search(r'<description>(.*?)</description>', response, re.DOTALL)
        if not description_match:
            raise ValueError("LLM response did not contain properly formatted description: " + response)
        
        return DirectoryDescriptionResult(description=description_match.group(1).strip())

_SYSTEM_PROMPT = """
You are a directory analyzer that creates comprehensive directory descriptions. You have background in software engineering and are able to understand the purpose of the code in the directory.

Your task is to analyze a directory structure and create a clear description that explains:
1. The overall purpose of the directory
2. How the contents work together
3. Any important patterns or conventions

Your description will be used to help LLM agents understand the purpose of the directory and its contents. So make it descriptive and helpful.

Format your response as follows:

<answer>
<reasoning>
A detailed explanation of your thought process for creating the description.
</reasoning>
<description>
A clear, concise description of the directory that explains its purpose, contents, and how they work together.
The description should help developers understand what they can find in this directory and how it's organized.
</description>
</answer>

Remember:
- Focus on the directory's role in the larger system
- Explain relationships between contained files/subdirectories
- Highlight important patterns or conventions
- Keep descriptions clear and concise
- use <thinking> tags to show your thought process
- public_interface and description tags are required and are placed at the end of your response
"""