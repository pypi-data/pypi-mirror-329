import pytest
import os
from stefan.tool.tool_create_multiple_files import CreateMultipleFilesToolDefinition
from stefan.execution_context import ExecutionContext

@pytest.fixture
def create_multiple_files_tool():
    return CreateMultipleFilesToolDefinition()

@pytest.fixture
def execution_context():
    return ExecutionContext()

def test_create_multiple_files_successful(create_multiple_files_tool, execution_context, tmp_path):
    args = {
        "file": [
            {"path": str(tmp_path / "file1.txt"), "content": "Content 1"},
            {"path": str(tmp_path / "file2.txt"), "content": "Content 2"},
            {"path": str(tmp_path / "nested/file3.txt"), "content": "Content 3"}
        ]
    }
    
    result = create_multiple_files_tool.execute_tool(args, execution_context)
    
    for file_data in args["file"]:
        file_path = file_data["path"]
        content = file_data["content"]
        assert os.path.exists(file_path)
        with open(file_path, 'r') as f:
            assert f.read() == content
        assert f"Successfully created file: {file_path}" in result

def test_create_multiple_files_empty_list(create_multiple_files_tool, execution_context, tmp_path):
    args = {"file": []}
    result = create_multiple_files_tool.execute_tool(args, execution_context)
    assert result == []

def test_create_multiple_files_with_special_characters(create_multiple_files_tool, execution_context, tmp_path):
    args = {
        "file": [
            {"path": str(tmp_path / "special1.txt"), "content": "Line 1\nLine 2\nSpecial: !@#$%^&*()"},
            {"path": str(tmp_path / "special2.txt"), "content": "Tab\tNewline\n"}
        ]
    }
    
    result = create_multiple_files_tool.execute_tool(args, execution_context)
    
    for file_data in args["file"]:
        file_path = file_data["path"]
        content = file_data["content"]
        assert os.path.exists(file_path)
        with open(file_path, 'r') as f:
            assert f.read() == content