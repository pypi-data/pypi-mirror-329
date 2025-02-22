import pytest
from stefan.execution_context import ExecutionContext
from stefan.project_configuration import ProjectContext
from stefan.tool.tool_show_directory import ShowDirectoryToolDefinition
from pathlib import Path

from stefan.tests.fixtures.dummy_project_context import create_dummy_project_context

@pytest.fixture
def project_context(tmp_path):
    return create_dummy_project_context(
        path=str(tmp_path),
        exclude_patterns=[".*", "__pycache__", ".git", ".kpmcoder", "__init__.py", ".stefan_output/**"],
        include_patterns=["*.py", "*.txt"],
    )

@pytest.fixture
def execution_context(project_context: ProjectContext):
    return ExecutionContext.test(project_context=project_context)

@pytest.fixture
def setup_test_directory(tmp_path):
    # Create a test directory structure
    test_dir = tmp_path / 'test_dir'
    test_dir.mkdir()
    
    # Create some test files and directories
    (test_dir / 'file1.txt').write_text('content1')
    (test_dir / 'file2.py').write_text('content2')
    
    # Create a subdirectory with files
    sub_dir = test_dir / 'subdir'
    sub_dir.mkdir()
    (sub_dir / 'file3.py').write_text('content3')
    (sub_dir / 'file4.txt').write_text('content4')
    
    # Create some excluded directories and files
    excluded_dir = test_dir / '__pycache__'
    excluded_dir.mkdir()
    (excluded_dir / 'cache.pyc').write_text('cache')
    
    (test_dir / '__init__.py').write_text('')
    
    return test_dir

@pytest.fixture
def tool():
    return ShowDirectoryToolDefinition()

def test_show_directory_basic(tool, execution_context, setup_test_directory):
    result = tool.execute_tool({"directory": str(setup_test_directory)}, execution_context)
    
    expected_output = (
        "# Table of Contents\n"
        "- file1.txt\n"
        "- file2.py\n"
        "- subdir/file3.py\n"
        "- subdir/file4.txt"
    )
    assert result == expected_output

def test_show_directory_with_postfix(tool, execution_context, setup_test_directory):
    result = tool.execute_tool(
        {"directory": str(setup_test_directory), "postfix": '.py'},
        context=execution_context,
    )
    
    expected_output = (
        "# Table of Contents\n"
        "- file2.py\n"
        "- subdir/file3.py"
    )
    assert result == expected_output

def test_show_directory_with_custom_include_patterns(setup_test_directory):
    project_context = create_dummy_project_context(str(setup_test_directory), include_patterns=["*.txt"])
    execution_context = ExecutionContext.test(project_context=project_context)

    tool = ShowDirectoryToolDefinition()
    
    result = tool.execute_tool({"directory": str(setup_test_directory)}, execution_context)
    
    expected_output = (
        "# Table of Contents\n"
        "- file1.txt\n"
        "- subdir/file4.txt"
    )
    assert result == expected_output

def test_show_directory_nonexistent(tool, execution_context):
    result = tool.execute_tool({"directory": 'nonexistent_directory'}, execution_context)
    assert "Error: Directory 'nonexistent_directory' does not exist" in result

def test_excluded_directories(tool, execution_context, setup_test_directory):
    result = tool.execute_tool({"directory": str(setup_test_directory)}, execution_context)
    assert '__pycache__' not in result
    assert 'cache.pyc' not in result

def test_excluded_files(tool, execution_context, setup_test_directory):
    result = tool.execute_tool({"directory": str(setup_test_directory)}, execution_context)
    assert '__init__.py' not in result

def test_empty_directory(tool, execution_context, tmp_path):
    empty_dir = tmp_path / 'empty_dir'
    empty_dir.mkdir()
    result = tool.execute_tool({"directory": str(empty_dir)}, execution_context)
    assert result == "No files found in directory"

def test_empty_directory_with_postfix(tool, execution_context, tmp_path):
    empty_dir = tmp_path / 'empty_dir'
    empty_dir.mkdir()
    result = tool.execute_tool(
        {"directory": str(empty_dir), "postfix": '.py'},
        context=execution_context,
    )
    assert result == "No files matching patterns: *.py found in directory"

def test_custom_exclude_patterns(setup_test_directory):
    project_context = create_dummy_project_context(
        path=str(setup_test_directory), 
        exclude_patterns=["*.txt", "__pycache__", "*.pyc", "__init__.py", ".stefan_output/**"]
    )
    execution_context = ExecutionContext.test(project_context=project_context)
    tool = ShowDirectoryToolDefinition()
    
    result = tool.execute_tool({"directory": str(setup_test_directory)}, execution_context)
    
    expected_output = (
        "# Table of Contents\n"
        "- file2.py\n"
        "- subdir/file3.py"
    )
    assert result == expected_output

def test_exclude_directory_with_pattern(setup_test_directory):
    # Create a context directory
    context_dir = setup_test_directory / 'context'
    context_dir.mkdir()
    (context_dir / 'file.py').write_text('content')
    
    project_context = create_dummy_project_context(
        path=Path(setup_test_directory),
        exclude_patterns=["context/**"],  # Exclude context directory and all its contents
        include_patterns=["*.py"]
    )
    execution_context = ExecutionContext.test(project_context=project_context)
    
    tool = ShowDirectoryToolDefinition()
    result = tool.execute_tool({"directory": str(setup_test_directory)}, execution_context)
    
    assert 'context' not in result
    assert 'file.py' not in result
