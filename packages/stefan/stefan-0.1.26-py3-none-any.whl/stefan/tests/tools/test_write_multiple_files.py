import pytest
import os
from stefan.tool.tool_write_multiple_files import WriteMultipleFilesToolDefinition
from stefan.execution_context import ExecutionContext

@pytest.fixture
def write_multiple_files_tool():
    return WriteMultipleFilesToolDefinition()

@pytest.fixture
def context():
    return ExecutionContext()

def test_write_multiple_files_successful(write_multiple_files_tool, context, tmp_path):
    # Test writing to multiple files
    file1_path = str(tmp_path / "file1.txt")
    file2_path = str(tmp_path / "file2.txt")
    
    args = {
        "file": [
            {"path": file1_path, "content": "Content for file 1"},
            {"path": file2_path, "content": "Content for file 2"}
        ]
    }
    
    result = write_multiple_files_tool.execute_tool(args, context)
    
    assert "Successfully wrote to file" in result
    assert file1_path in result
    assert file2_path in result
    
    with open(file1_path, 'r') as f:
        assert f.read() == "Content for file 1"
    with open(file2_path, 'r') as f:
        assert f.read() == "Content for file 2"

def test_write_multiple_files_nested_directories(write_multiple_files_tool, context, tmp_path):
    # Test writing to files in nested directories
    file1_path = str(tmp_path / "dir1" / "file1.txt")
    file2_path = str(tmp_path / "dir1" / "dir2" / "file2.txt")
    
    args = {
        "file": [
            {"path": file1_path, "content": "Content 1"},
            {"path": file2_path, "content": "Content 2"}
        ]
    }
    
    result = write_multiple_files_tool.execute_tool(args, context)
    
    assert "Successfully wrote to file" in result
    assert os.path.exists(file1_path)
    assert os.path.exists(file2_path)

def test_write_multiple_files_empty_content(write_multiple_files_tool, context, tmp_path):
    # Test writing empty content to files
    file1_path = str(tmp_path / "empty1.txt")
    file2_path = str(tmp_path / "empty2.txt")
    
    args = {
        "file": [
            {"path": file1_path, "content": ""},
            {"path": file2_path, "content": ""}
        ]
    }
    
    result = write_multiple_files_tool.execute_tool(args, context)
    
    assert "Successfully wrote to file" in result
    assert os.path.exists(file1_path)
    assert os.path.exists(file2_path)
    assert os.path.getsize(file1_path) == 0
    assert os.path.getsize(file2_path) == 0

def test_write_multiple_files_partial_failure(write_multiple_files_tool, context, tmp_path):
    # Test when some files succeed and others fail
    file1_path = str(tmp_path / "success.txt")
    file2_path = str(tmp_path / "no_access" / "fail.txt")
    
    # Create read-only directory
    no_access_dir = tmp_path / "no_access"
    no_access_dir.mkdir()
    os.chmod(no_access_dir, 0o444)
    
    args = {
        "file": [
            {"path": file1_path, "content": "Success content"},
            {"path": file2_path, "content": "Fail content"}
        ]
    }
    
    result = write_multiple_files_tool.execute_tool(args, context)
    
    assert "Successfully wrote to file" in result
    assert "Error writing to file" in result
    assert os.path.exists(file1_path)
    assert not os.path.exists(file2_path)

def test_write_multiple_files_special_characters(write_multiple_files_tool, context, tmp_path):
    # Test writing special characters to multiple files
    file1_path = str(tmp_path / "special1.txt")
    file2_path = str(tmp_path / "special2.txt")
    
    args = {
        "file": [
            {"path": file1_path, "content": "Special chars: !@#$%^&*()\nMultiple\nLines"},
            {"path": file2_path, "content": "More €£¥ symbols\tand\ttabs"}
        ]
    }
    
    result = write_multiple_files_tool.execute_tool(args, context)
    
    assert "Successfully wrote to file" in result
    with open(file1_path, 'r') as f:
        assert f.read() == "Special chars: !@#$%^&*()\nMultiple\nLines"
    with open(file2_path, 'r') as f:
        assert f.read() == "More €£¥ symbols\tand\ttabs"