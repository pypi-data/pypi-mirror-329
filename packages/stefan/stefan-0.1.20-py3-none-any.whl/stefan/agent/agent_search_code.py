from __future__ import annotations
import inspect
import os
from typing import Dict, List

from stefan.agent.agent_definition import AgentDefinition
from stefan.agent.prompt_template import PromptTemplate
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.tool.tool_attempt_completion import AttemptCompletionToolDefinition
from stefan.tool.tool_read_file import ReadFileToolDefinition
from stefan.tool.tool_read_multiple_files import ReadMultipleFilesToolDefinition
from stefan.tool.tool_rip_grep import RipGrepToolDefinition
from stefan.tool.tool_show_directory import ShowDirectoryToolDefinition
from stefan.tool.tool_definition import ToolDefinition
from stefan.utils.multiline import multiline

class SearchCodeAgent(AgentDefinition):
    name: str = "agent_search_code"
    description: str = multiline("""
        An agent specialized in complex code search tasks. It can perform relevancy based search, full text search as well as full text search with relevancy. Compared with search tools this agent is more sophisticated and can perform more complex search tasks.
        """)
    parameters: Dict[str, str] = {
        "query": "(required) The search query describing what code elements to find. Can include file names, class names, method names, or general code patterns. Example: 'Find all usages of AnalyticsTracker.logCost method' or 'Search for classes where is used NetworkRequest to get some usage examples' or 'Find all relevant files for profile feature'", 
        "context": "(optional) Additional context about why the search is needed or how the results will be used. This helps the agent provide more relevant results and suggestions. Example: 'We plan to rename this method' or 'We are implementing new endpoint and need to know how to handle serialization' or 'Looking for profile-related implementations so we can add new method into profile screen'",
    }
    llm_tag: LLMTag = LLMTag.AGENT_SEARCH_CODE
    usage: str = multiline("""
        <agent_search_code>
            <query>...</query>
            <context>...</context>
        </agent_search_code>
        """)
    available_agents: List['AgentDefinition'] = []
    available_tools: List[ToolDefinition] = [
        ReadFileToolDefinition(),
        ReadMultipleFilesToolDefinition(),

        ShowDirectoryToolDefinition(),
        RipGrepToolDefinition(),

        AttemptCompletionToolDefinition(),
    ]

    def create_system_prompt(self, prompt_template: PromptTemplate, context: ExecutionContext) -> str:
        # Get the current working directory
        cwd = os.getcwd()

        # Get all project files
        all_project_files = ShowDirectoryToolDefinition().execute_tool(args={"directory": cwd}, context=context)

        # Format the system prompt
        return _SYSTEM_PROMPT.format(
            tools_use_prompt=prompt_template.tools_use_prompt,
            file_paths_rules_prompt=prompt_template.file_paths_rules_prompt,
            metadata_project_context_prompt=prompt_template.metadata_project_context_prompt,
            answer_format_prompt=prompt_template.answer_format_prompt,
            all_project_files=all_project_files,
            cwd=cwd,
        )

_SYSTEM_PROMPT = """
You are an AI agent specialized in complex code search tasks. Your goal is to find relevant files for provided query. You will use combination of tools provided to you to find most relevant files for the given query and context. You have access to various search tools and should use them effectively to provide comprehensive results.

You will receive two inputs:
<query>...</query>
<context>...</context>
which you will use to find most relevant files for the given query and context.

====

## Instructions

Follow these steps to complete the search task:

1. Analyze the query and context to understand the search requirements.
2. Plan your search strategy.
4. For each tool use:
   a. Explain your reasoning for using it
   b. Describe the expected results
   c. Analyze the actual results
5. Reason about the results and provide recommendations or insights based on the search results and the given context
6. If you are not sure about the results, then you can start over and use different tools or different search strategy
7. If you started over more then 3 times, then you should for clarification
7. If you are satisfied with results then you will write summary of your findings and provide all relevant files with full file paths

====

{tools_use_prompt}

====

{file_paths_rules_prompt}

====

{metadata_project_context_prompt}

====

# All project files

{all_project_files}

====

## Response format

Present your findings and reasoning in the following format:
<answer>
    <attempt_completion>
        <response>
        Your detailed response here, including:
        - Analysis of the query and context
        - Explanation of search strategy
        - Results and analysis for each search technique
        - Synthesis of findings
        - Recommendations or insights
        </response>
        <file>
            <path>file path</path>
            <description>reason why this file is relevant</description>
        </file>
        <file>
            <path>file path</path>
            <description>reason why this file is relevant</description>
        </file>
    </attempt_completion>
</answer>

====

OUTPUT FORMAT

{answer_format_prompt}

====

Remember to use the available tools effectively and provide detailed explanations for your reasoning and findings. Your goal is to deliver comprehensive and relevant results that address the query and context provided.
"""
