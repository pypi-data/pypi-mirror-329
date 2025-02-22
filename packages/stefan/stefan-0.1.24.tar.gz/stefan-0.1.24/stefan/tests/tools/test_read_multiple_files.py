import pytest
import os
from stefan.tool.tool_read_multiple_files import ReadMultipleFilesToolDefinition
from stefan.execution_context import ExecutionContext

@pytest.fixture
def read_multiple_files_tool():
    return ReadMultipleFilesToolDefinition()

@pytest.fixture
def execution_context():
    return ExecutionContext(workspace_root="")

@pytest.fixture
def test_files(tmp_path):
    # Create multiple temporary files with content
    file_paths = []
    
    # Create first test file
    file1_path = tmp_path / "test1.txt"
    with open(file1_path, "w") as f:
        f.write("Content of file 1")
    file_paths.append(str(file1_path))
    
    # Create second test file
    file2_path = tmp_path / "test2.txt"
    with open(file2_path, "w") as f:
        f.write("Content of file 2")
    file_paths.append(str(file2_path))
    
    return file_paths

def test_read_multiple_files_successful(read_multiple_files_tool, test_files, execution_context):
    # Test successful reading of multiple files
    result = read_multiple_files_tool.execute_tool({"path": test_files}, execution_context)
    expected_result = (
        f'File: {test_files[0]}\n<file_content>\nContent of file 1\n</file_content>\n'
        f'File: {test_files[1]}\n<file_content>\nContent of file 2\n</file_content>\n'
    )
    assert result == expected_result

def test_read_multiple_files_with_nonexistent(read_multiple_files_tool, test_files, execution_context):
    # Test reading when one file doesn't exist
    test_files.append("nonexistent_file.txt")
    result = read_multiple_files_tool.execute_tool({"path": test_files}, execution_context)
    assert "Error reading nonexistent_file.txt: " in result
    assert "Content of file 1" in result
    assert "Content of file 2" in result

def test_read_multiple_files_empty(read_multiple_files_tool, tmp_path, execution_context):
    # Test reading empty files
    empty_file = tmp_path / "empty.txt"
    empty_file.touch()
    result = read_multiple_files_tool.execute_tool({"path": [str(empty_file)]}, execution_context)
    expected_result = f'File: {str(empty_file)}\n<file_content>\n\n</file_content>\n'
    assert result == expected_result

def test_read_multiple_files_with_different_content(read_multiple_files_tool, tmp_path, execution_context):
    # Test reading files with different content types
    file_paths = []
    
    # File with multiple lines
    multiline_file = tmp_path / "multiline.txt"
    multiline_content = "Line 1\nLine 2\nLine 3"
    with open(multiline_file, "w") as f:
        f.write(multiline_content)
    file_paths.append(str(multiline_file))
    
    # File with special characters
    special_file = tmp_path / "special.txt"
    special_content = "Special chars: !@#$%^&*()"
    with open(special_file, "w") as f:
        f.write(special_content)
    file_paths.append(str(special_file))
    
    result = read_multiple_files_tool.execute_tool({"path": file_paths}, execution_context)
    assert multiline_content in result
    assert special_content in result

def test_read_multiple_files_permissions(read_multiple_files_tool, tmp_path, execution_context):
    # Test reading files with different permissions
    no_access_file = tmp_path / "no_access.txt"
    with open(no_access_file, "w") as f:
        f.write("Secret content")
    os.chmod(no_access_file, 0o200)  # Write-only permission
    
    result = read_multiple_files_tool.execute_tool({"path": [str(no_access_file)]}, execution_context)
    assert "Error reading" in result
    assert "Permission denied" in result