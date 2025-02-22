import pytest
import os
from stefan.tool.tool_read_file import ReadFileToolDefinition
from stefan.execution_context import ExecutionContext

@pytest.fixture
def read_file_tool():
    return ReadFileToolDefinition()

@pytest.fixture
def execution_context():
    return ExecutionContext(workspace_root="")

@pytest.fixture
def test_file(tmp_path):
    # Create a temporary file with some content
    file_path = tmp_path / "test.txt"
    with open(file_path, "w") as f:
        f.write("Hello, World!")
    return str(file_path)

def test_read_file_successful(read_file_tool, test_file, execution_context):
    # Test successful file reading
    result = read_file_tool.execute_tool({"path": test_file}, execution_context)
    assert result == "<file_content>\nHello, World!\n</file_content>"

def test_read_file_nonexistent(read_file_tool, execution_context):
    # Test reading a non-existent file
    with pytest.raises(FileNotFoundError):
        read_file_tool.execute_tool({"path": "nonexistent_file.txt"}, execution_context)

def test_read_empty_file(read_file_tool, tmp_path, execution_context):
    # Test reading an empty file
    empty_file = tmp_path / "empty.txt"
    empty_file.touch()
    result = read_file_tool.execute_tool({"path": str(empty_file)}, execution_context)
    assert result == "<file_content>\n\n</file_content>"

def test_read_file_with_multiple_lines(read_file_tool, tmp_path, execution_context):
    # Test reading a file with multiple lines
    multi_line_file = tmp_path / "multiline.txt"
    content = "Line 1\nLine 2\nLine 3"
    with open(multi_line_file, "w") as f:
        f.write(content)
    result = read_file_tool.execute_tool({"path": str(multi_line_file)}, execution_context)
    assert result == f"<file_content>\n{content}\n</file_content>"

def test_read_file_permissions(read_file_tool, tmp_path, execution_context):
    # Test reading a file with no read permissions
    no_access_file = tmp_path / "no_access.txt"
    with open(no_access_file, "w") as f:
        f.write("Secret content")
    os.chmod(no_access_file, 0o200)  # Write-only permission
    
    with pytest.raises(PermissionError):
        read_file_tool.execute_tool({"path": str(no_access_file)}, execution_context)