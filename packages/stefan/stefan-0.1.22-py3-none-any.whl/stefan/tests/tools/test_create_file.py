import pytest
import os
from stefan.tests.fixtures.dummy_project_context import create_dummy_project_context
from stefan.tool.tool_create_file import CreateFileToolDefinition

@pytest.fixture
def project_context(tmp_path):
    return create_dummy_project_context(path=str(tmp_path))

@pytest.fixture
def create_file_tool():
    return CreateFileToolDefinition()

def test_create_file_successful(create_file_tool, tmp_path, project_context):
    # Test creating a file in an existing directory
    file_path = str(tmp_path / "test.txt")
    content = "Hello, World!"

    args = {
        "file_path": file_path,
        "content": content,
    }
    result = create_file_tool.execute_tool(args, project_context)
    
    assert "Successfully created file" in result
    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        assert f.read() == content

def test_create_file_in_new_directory(create_file_tool, tmp_path, project_context):
    # Test creating a file in a new nested directory
    nested_path = tmp_path / "new_dir" / "sub_dir"
    file_path = str(nested_path / "test.txt")
    content = "Test content"
    
    args = {
        "file_path": file_path,
        "content": content,
    }
    result = create_file_tool.execute_tool(args, project_context)
    
    assert "Successfully created file" in result
    assert os.path.exists(file_path)
    with open(file_path, 'r') as f:
        assert f.read() == content

def test_create_file_with_empty_content(create_file_tool, tmp_path, project_context):
    # Test creating a file with empty content
    file_path = str(tmp_path / "empty.txt")
    content = ""
    
    args = {
        "file_path": file_path,
        "content": content,
    }
    result = create_file_tool.execute_tool(args, project_context)
    
    assert "Successfully created file" in result
    assert os.path.exists(file_path)
    assert os.path.getsize(file_path) == 0

def test_create_file_with_special_characters(create_file_tool, tmp_path, project_context):
    # Test creating a file with special characters and multiple lines
    file_path = str(tmp_path / "special.txt")
    content = "Line 1\nLine 2\nSpecial chars: !@#$%^&*()"
    
    args = {
        "file_path": file_path,
        "content": content,
    }
    result = create_file_tool.execute_tool(args, project_context)
    
    assert "Successfully created file" in result
    with open(file_path, 'r') as f:
        assert f.read() == content

def test_create_file_permission_error(create_file_tool, tmp_path, project_context):
    # Test creating a file in a directory without write permissions
    no_access_dir = tmp_path / "no_access"
    no_access_dir.mkdir()
    os.chmod(no_access_dir, 0o444)  # Read-only permission
    
    file_path = str(no_access_dir / "test.txt")
    content = "Test content"
    
    args = {
        "file_path": file_path,
        "content": content,
    }
    result = create_file_tool.execute_tool(args, project_context)
    
    assert "Error creating file" in result

def test_create_file_existing_directory(create_file_tool, tmp_path, project_context):
    # Test that creating a file doesn't overwrite existing directories
    dir_path = tmp_path / "existing_dir"
    dir_path.mkdir()
    
    file_path = str(dir_path)
    content = "Test content"
    
    args = {
        "file_path": file_path,
        "content": content,
    }
    result = create_file_tool.execute_tool(args, project_context)
    
    assert "Error creating file" in result
    assert os.path.isdir(dir_path)  # Directory should still exist