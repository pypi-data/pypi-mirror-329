from pathlib import Path
import re
from typing import List
from pydantic import BaseModel
from concurrent.futures import ThreadPoolExecutor
import asyncio

from stefan.code_search.file_system_nodes import FileNode
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_model import LLM_MODEL
from stefan.code_search.llm.llm_executor import LLMExecutor
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.utils.async_execution import AsyncExecution

class FileRelevancyResult(BaseModel):
    file_path: Path
    is_relevant: bool
    relevance_score: float
    explanation: str

class FileRelevancyLLMProcessor:
    def __init__(self, llm_executor: LLMExecutor, async_execution: AsyncExecution):
        self.llm_executor = llm_executor
        self.async_execution = async_execution

    def determine_relevancy(
        self,
        query: str,
        file_nodes: List[FileNode],
        context: ExecutionContext,
    ) -> List[FileRelevancyResult]:
        args_list = [(query, file_node.path, context) for file_node in file_nodes]
        return self.async_execution.run_async_tasks_in_executor(self._determine_relevancy_for_single_file, *args_list)

    def _determine_relevancy_for_single_file(
        self,
        query: str,
        file_path: Path,
        context: ExecutionContext,
    ) -> FileRelevancyResult:
        """
        Determine the relevancy of a file for a given query using LLM.
        Returns a FileRelevancyResult containing a boolean, a score, and an explanation.
        """
        # Load file content
        with open(file_path, "r") as file:
            file_content = file.read()
        
        messages = [
            {
                "role": "system",
                "content": _SYSTEM_PROMPT_FILE_RELEVANCY,
            },
            {
                "role": "user",
                "content": f"Query: {query}\n\nFile: {file_path}\n\n{file_content}"
            }
        ]

        success_result, error = self.llm_executor.generate(
            tag=LLMTag.CODE_SEARCH_FILE_RELEVANCY,
            model=LLM_MODEL.OPEN_AI_4o_MINI,
            messages=messages,
            execution_context=context,
        ).unpack()

        # If there was an error, raise it - we don't want to skip this error
        if error is not None:
            raise error
        
        # Get response from LLM
        response = success_result.response

        # Extract relevancy information from the response
        reasoning_match = re.search(r'<reasoning>(.*?)</reasoning>', response, re.DOTALL)
        score_match = re.search(r'<score>(.*?)</score>', response, re.DOTALL)
        is_relevant_match = re.search(r'<is_relevant>(.*?)</is_relevant>', response, re.DOTALL)
        if not (reasoning_match and score_match and is_relevant_match):
            raise ValueError("LLM response did not contain properly formatted relevancy information: " + response)
        explanation = reasoning_match.group(1).strip()
        relevance_score = float(score_match.group(1).strip())
        is_relevant = is_relevant_match.group(1).strip().lower() == 'true'

        return FileRelevancyResult(
            file_path=file_path,
            is_relevant=is_relevant,
            relevance_score=relevance_score,
            explanation=explanation,
        )

_SYSTEM_PROMPT_FILE_RELEVANCY = """
You are a code analyzer that determines the relevancy of a file based on a given query.

Your task is to analyze the file content and decide if it is relevant to the query. Provide a relevance score between 0 and 1, and an explanation for your decision.

1 - The file is totally rrelevant to the query and it is exactly what the query asks for.
1..0.8 - The file is relevant to the query, but it is not exactly what the query asks for.
0.8..0.5 - The file may be relevant to the query.
0.5..0.3 - The file is probably not relevant to the query.
0.3..0 - The file is not relevant to the query.

Rules:
1. Consider the context of the query and the file content.
2. Evaluate if the file contains elements related to the query.
3. Provide a boolean indicating relevancy (true/false).
4. Assign a relevance score (0 to 1) based on the strength of the match.
5. Offer a clear explanation for your decision.

Format your response as follows:

<answer>
<reasoning>Reasoning why the file is relevant or not relevant to the query.</reasoning>
<score>0.85</score>
<is_relevant>true</is_relevant>
</answer>

Remember:
- Be concise and clear in your explanation.
- Use the relevance score to reflect the degree of match.
- Ensure the response is well-structured and follows the format.
- use <thinking> tags to show your thought process
- answer with reasoning, score and is_relevant tags are required and are placed at the end of your response
"""