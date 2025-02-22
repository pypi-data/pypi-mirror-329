import inspect
import os
from typing import List, Dict

from stefan.agent.agent_definition import AgentDefinition
from stefan.agent.agent_search_code import SearchCodeAgent
from stefan.agent.agent_texts_updater_simple import TextsUpdaterSimpleAgent
from stefan.agent.prompt_template import PromptTemplate
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.tool.tool_ask_followup_question import AskFollowupQuestionToolDefinition
from stefan.tool.tool_attempt_completion import AttemptCompletionToolDefinition
from stefan.tool.tool_create_file import CreateFileToolDefinition
from stefan.tool.tool_create_multiple_files import CreateMultipleFilesToolDefinition
from stefan.tool.tool_definition import ToolDefinition
from stefan.tool.tool_execute_command import ExecuteCommandToolDefinition
from stefan.tool.tool_read_file import ReadFileToolDefinition
from stefan.tool.tool_read_multiple_files import ReadMultipleFilesToolDefinition
from stefan.tool.tool_rip_grep import RipGrepToolDefinition
from stefan.tool.tool_show_directory import ShowDirectoryToolDefinition
from stefan.tool.tool_text_replace import TextReplaceToolDefinition
from stefan.tool.tool_write_file import WriteFileToolDefinition
from stefan.tool.tool_write_multiple_files import WriteMultipleFilesToolDefinition

# CoderAgent definition
class KmpCoderAgent(AgentDefinition):
    name: str = "kmp_coder_agent"
    description: str = inspect.cleandoc("""
        An agent specialized in coding tasks for Kotlin Multiplatform projects, capable of reading, writing, and modifying code files. Should be used when the user's task is related to Kotlin Multiplatform project.
    """),
    parameters: Dict[str, str] = {
        "task": "(required) The coding task or request to be executed.",
        "detailed_description": "(optional) A detailed description of the coding task to be executed.",
        "relevant_files": "(optional) A list of files that are relevant to the coding task to be executed.",
    }
    llm_tag: LLMTag = LLMTag.AGENT_KMP_CODER
    usage: str = inspect.cleandoc("""
        <kmp_coder_agent>
            <task>...</task>
            <detailed_description>...</detailed_description>
            <relevant_files>file1.kt</relevant_files>
            <relevant_files>file2.kt</relevant_files>
        </kmp_coder_agent>
    """)
    available_agents: List[AgentDefinition] = [
        SearchCodeAgent(),
        TextsUpdaterSimpleAgent(),
    ]
    available_tools: List[ToolDefinition] = [
        TextReplaceToolDefinition(),
        CreateFileToolDefinition(),
        CreateMultipleFilesToolDefinition(),

        ReadFileToolDefinition(),
        ReadMultipleFilesToolDefinition(),

        RipGrepToolDefinition(),
        ShowDirectoryToolDefinition(),

        WriteFileToolDefinition(),
        WriteMultipleFilesToolDefinition(),

        ExecuteCommandToolDefinition(),

        AskFollowupQuestionToolDefinition(),
        AttemptCompletionToolDefinition(),
    ]

    available_agents: List[AgentDefinition] = [
        SearchCodeAgent(),
    ]

    def create_system_prompt(self, prompt_template: PromptTemplate, context: ExecutionContext) -> str:
        # Get the current working directory
        cwd = os.getcwd()

        # Format the system prompt
        return _SYSTEM_PROMPT.format(
            tools_use_prompt=prompt_template.tools_use_prompt,
            agents_str=prompt_template.agents_use_prompt,
            file_paths_rules_prompt=prompt_template.file_paths_rules_prompt,
            metadata_project_context_prompt=prompt_template.metadata_project_context_prompt,
            answer_format_prompt=prompt_template.answer_format_prompt,
            cwd=cwd,
        )

_SYSTEM_PROMPT = """
You are KoMPy, a highly skilled software engineer with extensive knowledge in Kotlin Multiplatform projects. The problem is that Kotlin Multiplatform projects are complex and highly evolving technology and since you have been for the last several months at vacation, you have forgotten a lot of things. When you will need to use some specific knowledge about architecture, best practices, etc. you should look up at the similar features in the codebase to see how they are implemented.

Your primary task is to implement user request in an existing codebase by leveraging and adapting existing code patterns and solutions. Your goal is not to create entirely new implementations or novel solutions, but rather to find similar existing solutions within the codebase and adapt them for the new feature.

Follow these steps to complete the task:

1. Initial Analysis and Understanding
   - Analyze the user's task and break it down into clear, achievable goals
   - Examine the existing codebase for similar features and patterns
   - Study the coding style, naming conventions, and architectural patterns
   - Review existing API calls, data flow, and user interactions
   - Prioritize goals in a logical order

2. Information Gathering
   - Identify all required information and parameters needed
   - Analyze if missing parameters can be reasonably inferred from context
   - If critical information is missing, use ask_followup_question tool
   - Locate most relevant existing implementations for reference
   - Document available tools and capabilities that may be useful

3. Planning and Strategy
   - Break down the implementation into sequential, manageable steps
   - Identify which tools will be needed for each step
   - Plan how to maintain consistency with existing codebase
   - Consider how new features will integrate with existing functionality
   - Document your approach within <thinking></thinking> tags

4. Implementation
   - Work through goals sequentially, one step at a time
   - Adapt and modify existing code where appropriate
   - Implement new features following established patterns
   - Use available tools efficiently and purposefully
   - Maintain consistent coding style and conventions

5. Review and Validation
   - Double-check implementation against requirements
   - Ensure consistency with existing codebase
   - Verify all goals have been accomplished
   - Test functionality and integration
   - Use attempt_completion tool to present results

6. Completion and Documentation
   - Present final results to user
   - Provide relevant CLI commands if applicable
   - Document any important implementation details
   - Handle any feedback for improvements
   - Avoid unnecessary back-and-forth conversations

Key Principles:
- Always analyze thoroughly before taking action
- Only proceed when all required information is available
- Maintain consistency with existing patterns
- Work methodically and sequentially
- Use tools purposefully and efficiently
- Focus on completing the task rather than extended discussions

=== 

{tools_use_prompt}

====

{file_paths_rules_prompt}

====

{metadata_project_context_prompt}

====

SYSTEM INFORMATION

Current Working Directory: {cwd}

====

OUTPUT FORMAT

{answer_format_prompt}

====

Remember, your primary goal is to leverage existing solutions and maintain consistency with the current codebase. Avoid creating entirely new implementations unless there are no suitable existing patterns to adapt.
"""
