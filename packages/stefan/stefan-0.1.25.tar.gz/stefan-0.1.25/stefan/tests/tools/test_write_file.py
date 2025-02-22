import pytest
import os
from stefan.tool.tool_write_file import WriteFileToolDefinition
from stefan.execution_context import ExecutionContext

@pytest.fixture
def write_file_tool():
    return WriteFileToolDefinition()

@pytest.fixture
def context():
    return ExecutionContext()

def test_write_file_successful(write_file_tool, context, tmp_path):
    # Create an initial file
    file_path = str(tmp_path / "test.txt")
    with open(file_path, 'w') as f:
        f.write("Initial content")
    
    content = "Hello, World!"
    result = write_file_tool.execute_tool({"file_path": file_path, "content": content}, context)
    
    assert "Successfully wrote to file" in result
    with open(file_path, 'r') as f:
        assert f.read() == content

def test_write_file_append_mode(write_file_tool, context, tmp_path):
    # Test appending to an existing file
    file_path = str(tmp_path / "append.txt")
    initial_content = "Initial line\n"
    append_content = "Appended line"
    
    with open(file_path, 'w') as f:
        f.write(initial_content)
    
    result = write_file_tool.execute_tool(
        {"file_path": file_path, "content": append_content, "mode": 'a'},
        context
    )
    
    assert "Successfully wrote to file" in result
    with open(file_path, 'r') as f:
        content = f.read()
        assert content == initial_content + append_content

def test_write_file_invalid_mode(write_file_tool, context, tmp_path):
    # Test invalid write mode
    file_path = str(tmp_path / "test.txt")
    with open(file_path, 'w') as f:
        f.write("Initial content")
    
    result = write_file_tool.execute_tool(
        {"file_path": file_path, "content": "New content", "mode": 'x'},
        context
    )
    
    assert "Error: Invalid mode" in result

def test_write_file_permission_error(write_file_tool, context, tmp_path):
    # Test writing to a read-only file
    file_path = str(tmp_path / "readonly.txt")
    with open(file_path, 'w') as f:
        f.write("Initial content")
    
    os.chmod(file_path, 0o444)  # Read-only permission
    
    result = write_file_tool.execute_tool(
        {"file_path": file_path, "content": "New content"},
        context
    )
    
    assert "Error writing to file" in result

def test_write_file_special_characters(write_file_tool, context, tmp_path):
    # Test writing special characters
    file_path = str(tmp_path / "special.txt")
    with open(file_path, 'w') as f:
        f.write("Initial content")
    
    content = "Special chars: !@#$%^&*()\nMultiple\nLines"
    result = write_file_tool.execute_tool(
        {"file_path": file_path, "content": content},
        context
    )
    
    assert "Successfully wrote to file" in result
    with open(file_path, 'r') as f:
        assert f.read() == content