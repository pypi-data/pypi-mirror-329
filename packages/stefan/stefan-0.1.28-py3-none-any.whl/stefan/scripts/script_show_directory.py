from stefan.execution_context import ExecutionContextfrom stefan.project_configuration import ProjectContext
from stefan.tool.tool_show_directory import ShowDirectoryToolDefinition

def script_show_directory(project_context: ProjectContext):
    context = ExecutionContext.initial(current_agent=None, project_context=project_context)
    tool = ShowDirectoryToolDefinition()
    args = {
        "directory": "."
    }
    print(tool.execute_tool(args, context))
