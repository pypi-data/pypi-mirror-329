import inspect

from pydantic import BaseModel
from stefan.code_search.llm.llm_executor import LLMExecutor
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_model import LLM_MODEL
import re

from stefan.code_search.llm.llm_tag import LLMTag

class FileDescriptionResult(BaseModel):
    public_interface: str
    description: str

class FileDescriptionLLMProcessor:

    def __init__(self, llm_executor: LLMExecutor):
        self.llm_executor = llm_executor

    def extract_public_interface_and_description(self, file_content: str, file_path: str) -> FileDescriptionResult:
        """
        Extract public interface information from file content using LLM.
        Returns XML-formatted string containing the public interface details.
        """
        messages = [
            {
                "role": "system",
                "content": _SYSTEM_PROMPT_FILE_DESCRIPTION,
            },
            {
                "role": "user",
                "content": inspect.cleandoc(f"""
                    Analyze this code and extract its public interface:
                                                            
                    File: {file_path}

                    {file_content}
                """)
            }
        ]

        success_result, error = self.llm_executor.generate(
            tag=LLMTag.CODE_SEARCH_FILE_DESCRIPTION,
            model=LLM_MODEL.OPEN_AI_4o_MINI,
            messages=messages,
            execution_context=ExecutionContext.empty(),
        ).unpack()

        # If there was an error, raise it - we don't want to skip this error
        if error is not None:
            raise error
        
        # Get response from LLM
        response = success_result.response

        # Extract public_interface using regex
        xml_match = re.search(r'<public_interface>(.*?)</public_interface>', response, re.DOTALL)
        if not xml_match:
            raise ValueError("LLM response did not contain properly formatted XML: " + response)
        public_interface = xml_match.group(1) # Return only the content between tags
    
        # Extract description using regex
        description_match = re.search(r'<description>(.*?)</description>', response, re.DOTALL)
        if not description_match:
            raise ValueError("LLM response did not contain properly formatted XML: " + response)
        description = description_match.group(1) # Return only the content between tags
    
        return FileDescriptionResult(public_interface=public_interface, description=description)

_SYSTEM_PROMPT_FILE_DESCRIPTION = """
You are a code analyzer that extracts public interfaces from source code.

Your task is to create a clean, documented version of the public interface while maintaining the original code structure.

Rules:
1. Keep the original code structure and syntax
2. Include only public/protected elements that could be called from other files
3. Add or enhance docstrings and type hints if missing
4. Skip private methods and implementation details
5. For long files, include only the method signatures and documentation
6. Maintain imports if they're relevant to the public interface

Format your response as follows:

<public_interface>
# Keep all imports
from typing import List, Optional

class MyClass:
    \"\"\"
    Enhanced class documentation explaining purpose and usage.
    \"\"\"
    
    def public_method(param1: str, param2: Optional[int] = None) -> bool:
        \"\"\"
        Enhanced method documentation.
        
        Args:
            param1: Description of param1
            param2: Description of param2
            
        Returns:
            Description of return value
        \"\"\"
        pass  # Implementation details omitted

# Global variables/constants (if any)
MAX_RETRIES: int = 3  # Description of constant
</public_interface>
<description>
This is a description of the file. It mentions the purpose of the file and all required informations for coding agent to use this file.
</description>

Remember:
- Maintain language-specific documentation styles
- Include type hints where possible
- Add clear docstrings for all public elements
- Skip implementation details with 'pass' or '...'
- Keep only public/protected interface elements
- use <thinking> tags to show your thought process
- public_interface and description tags are required and are placed at the end of your response
"""