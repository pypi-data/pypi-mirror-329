import pytest
from pathlib import Path
from datetime import datetime
import json
import tempfile

from stefan.code_search.file_system_nodes import FileNode, DirectoryNode, FileSystemTree
from stefan.code_search.code_search_persistence import CodeSearchPersistence

@pytest.fixture
def sample_tree():
    """Create a sample file tree for testing"""
    # Create a simple tree structure
    file1 = FileNode(
        path=Path("/test/file1.txt"),
        name="file1.txt",
        last_modified=datetime(2024, 1, 1, 12, 0),
        file_size=100,
        file_hash="hash1"
    )
    
    file2 = FileNode(
        path=Path("/test/dir1/file2.py"),
        name="file2.py",
        last_modified=datetime(2024, 1, 2, 12, 0),
        file_size=200,
        file_hash="hash2"
    )
    
    dir1 = DirectoryNode(
        path=Path("/test/dir1"),
        name="dir1",
        last_modified=datetime(2024, 1, 3, 12, 0),
        children=[file2]
    )
    
    root = DirectoryNode(
        path=Path("/test"),
        name="test",
        last_modified=datetime(2024, 1, 4, 12, 0),
        children=[file1, dir1]
    )
    
    return FileSystemTree(root=root)

def test_save_tree(sample_tree: FileSystemTree):
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
        temp_path = Path(tmp_file.name)
    
    try:
        # Save the tree
        CodeSearchPersistence.save_tree(sample_tree, temp_path)
        
        # Read the saved JSON and verify its structure
        with open(temp_path) as f:
            saved_data = json.load(f)
        
        # Basic structure checks
        assert saved_data['_type'] == 'DirectoryNode'
        assert saved_data['name'] == 'test'
        assert 'should_be_recalculated' not in saved_data
        assert len(saved_data['children']) == 2
        
        # Check first child (file1)
        file1_data = saved_data['children'][0]
        assert file1_data['_type'] == 'FileNode'
        assert file1_data['name'] == 'file1.txt'
        assert file1_data['file_hash'] == 'hash1'
        
        # Check second child (dir1)
        dir1_data = saved_data['children'][1]
        assert dir1_data['_type'] == 'DirectoryNode'
        assert dir1_data['name'] == 'dir1'
        assert len(dir1_data['children']) == 1
        
    finally:
        temp_path.unlink()

def test_load_tree(sample_tree: FileSystemTree):
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
        temp_path = Path(tmp_file.name)
    
    try:
        # Save and then load the tree
        CodeSearchPersistence.save_tree(sample_tree, temp_path)
        loaded_tree = CodeSearchPersistence.try_load_tree(temp_path)
        
        # Verify the loaded tree structure
        assert isinstance(loaded_tree, FileSystemTree)
        assert loaded_tree.root.name == 'test'
        assert loaded_tree.root.should_be_recalculated is None
        assert len(loaded_tree.root.children) == 2
        
        # Check first child (file1)
        file1 = loaded_tree.root.children[0]
        assert isinstance(file1, FileNode)
        assert file1.name == 'file1.txt'
        assert file1.file_hash == 'hash1'
        assert file1.file_size == 100
        assert file1.should_be_recalculated is None
        
        # Check second child (dir1) and its nested file
        dir1 = loaded_tree.root.children[1]
        assert isinstance(dir1, DirectoryNode)
        assert dir1.name == 'dir1'
        assert len(dir1.children) == 1
        
        file2 = dir1.children[0]
        assert isinstance(file2, FileNode)
        assert file2.name == 'file2.py'
        assert file2.file_hash == 'hash2'
        assert file2.file_size == 200
        
    finally:
        temp_path.unlink()

def test_load_tree_with_invalid_type():
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
        temp_path = Path(tmp_file.name)
        # Write invalid node type
        json_data = {
            "_type": "InvalidNode",
            "path": "/test",
            "name": "test",
            "last_modified": "2024-01-01T12:00:00"
        }
        json.dump(json_data, tmp_file)
        tmp_file.flush()  # Ensure all data is written
    
    try:
        with pytest.raises(ValueError, match="Unknown node type: InvalidNode"):
            CodeSearchPersistence.try_load_tree(temp_path)
    finally:
        temp_path.unlink()

def test_datetime_serialization(sample_tree: DirectoryNode):
    with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as tmp_file:
        temp_path = Path(tmp_file.name)
    
    try:
        # Save and load the tree
        CodeSearchPersistence.save_tree(sample_tree, temp_path)
        loaded_tree = CodeSearchPersistence.try_load_tree(temp_path)
        
        # Verify datetime fields are correctly preserved
        assert loaded_tree.root.last_modified == datetime(2024, 1, 4, 12, 0)
        assert loaded_tree.root.children[0].last_modified == datetime(2024, 1, 1, 12, 0)
        assert loaded_tree.root.children[1].last_modified == datetime(2024, 1, 3, 12, 0)
        assert loaded_tree.root.children[1].children[0].last_modified == datetime(2024, 1, 2, 12, 0)
        
    finally:
        temp_path.unlink()
