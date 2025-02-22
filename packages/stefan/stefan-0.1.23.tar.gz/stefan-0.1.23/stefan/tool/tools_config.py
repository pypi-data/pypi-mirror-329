from stefan.tool.tool_create_file import CreateFileToolDefinition
from stefan.tool.tool_create_multiple_files import CreateMultipleFilesToolDefinition
from stefan.tool.tool_full_text_search import FullTextSearchToolDefinition
from stefan.tool.tool_full_text_with_relevancy_search import FullTextWithRelevancySearchToolDefinition
from stefan.tool.tool_read_file import ReadFileToolDefinition
from stefan.tool.tool_read_multiple_files import ReadMultipleFilesToolDefinition
from stefan.tool.tool_search_code import SearchCodeToolDefinition
from stefan.tool.tool_show_directory import ShowDirectoryToolDefinition
from stefan.tool.tool_write_file import WriteFileToolDefinition
from stefan.tool.tool_write_multiple_files import WriteMultipleFilesToolDefinition
from stefan.tool.tool_ask_followup_question import AskFollowupQuestionToolDefinition
from stefan.tool.tool_attempt_completion import AttemptCompletionToolDefinition

AVAILABLE_TOOLS = [
    CreateFileToolDefinition(),
    CreateMultipleFilesToolDefinition(),
    ReadFileToolDefinition(),
    ReadMultipleFilesToolDefinition(),
    ShowDirectoryToolDefinition(),
    WriteFileToolDefinition(),
    WriteMultipleFilesToolDefinition(),
    SearchCodeToolDefinition(),
    FullTextSearchToolDefinition(),
    FullTextWithRelevancySearchToolDefinition(),
    AskFollowupQuestionToolDefinition(),
    AttemptCompletionToolDefinition(),
]

PLANNER_TOOLS = [
    ReadFileToolDefinition(),
    ReadMultipleFilesToolDefinition(),
    ShowDirectoryToolDefinition(),
    SearchCodeToolDefinition(),
    FullTextSearchToolDefinition(),
    FullTextWithRelevancySearchToolDefinition(),
    AskFollowupQuestionToolDefinition(),
    AttemptCompletionToolDefinition(),
]

CODER_TOOLS = AVAILABLE_TOOLS