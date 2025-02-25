from datetime import datetime
from pathlib import Path
import pytest
from stefan.code_search.file_system_nodes import FileSystemNode, FileNode, DirectoryNode, FileSystemTree

@pytest.fixture
def sample_file_node():
    return FileNode(
        name="test.py",
        path=Path("/test/test.py"),
        last_modified=datetime(2024, 1, 1),
        file_size=100,
        file_hash="abc123"
    )

@pytest.fixture
def sample_directory_node():
    return DirectoryNode(
        name="test_dir",
        path=Path("/test/test_dir"),
        last_modified=datetime(2024, 1, 1),
        children=[]
    )

class TestFileNode:
    def test_extension(self, sample_file_node):
        assert sample_file_node.extension == "py"
        
    def test_full_path(self, sample_file_node):
        assert sample_file_node.full_path == str(Path("/test/test.py").absolute())
        
    def test_no_extension(self):
        file_node = FileNode(
            name="testfile",
            path=Path("/test/testfile"),
            last_modified=datetime(2024, 1, 1),
            file_size=100,
            file_hash="abc123"
        )
        assert file_node.extension is None

class TestDirectoryNode:
    def test_files_and_directories(self):
        file1 = FileNode(
            name="test1.py",
            path=Path("/test/test1.py"),
            last_modified=datetime(2024, 1, 1),
            file_size=100,
            file_hash="abc123"
        )
        subdir = DirectoryNode(
            name="subdir",
            path=Path("/test/subdir"),
            last_modified=datetime(2024, 1, 1),
            children=[]
        )
        
        dir_node = DirectoryNode(
            name="test_dir",
            path=Path("/test/test_dir"),
            last_modified=datetime(2024, 1, 1),
            children=[file1, subdir]
        )
        
        assert len(dir_node.files) == 1
        assert len(dir_node.directories) == 1
        assert dir_node.files[0] == file1
        assert dir_node.directories[0] == subdir

class TestFileSystemTree:
    def test_all_files(self):
        # Create a nested structure:
        # root/
        #   ├── file1.py
        #   └── dir1/
        #       ├── file2.py
        #       └── dir2/
        #           └── file3.py
        
        file3 = FileNode(
            name="file3.py",
            path=Path("/root/dir1/dir2/file3.py"),
            last_modified=datetime(2024, 1, 1),
            file_size=100,
            file_hash="abc123"
        )
        
        dir2 = DirectoryNode(
            name="dir2",
            path=Path("/root/dir1/dir2"),
            last_modified=datetime(2024, 1, 1),
            children=[file3]
        )
        
        file2 = FileNode(
            name="file2.py",
            path=Path("/root/dir1/file2.py"),
            last_modified=datetime(2024, 1, 1),
            file_size=100,
            file_hash="abc123"
        )
        
        dir1 = DirectoryNode(
            name="dir1",
            path=Path("/root/dir1"),
            last_modified=datetime(2024, 1, 1),
            children=[file2, dir2]
        )
        
        file1 = FileNode(
            name="file1.py",
            path=Path("/root/file1.py"),
            last_modified=datetime(2024, 1, 1),
            file_size=100,
            file_hash="abc123"
        )
        
        root = DirectoryNode(
            name="root",
            path=Path("/root"),
            last_modified=datetime(2024, 1, 1),
            children=[file1, dir1]
        )
        
        tree = FileSystemTree(root=root)
        
        # This test will fail because all_files doesn't recursively traverse
        # It will only find file1.py and file2.py, but miss file3.py
        all_files = tree.all_files
        assert len(all_files) == 3  # Should be 3, but current implementation will only find 2
        assert file1 in all_files
        assert file2 in all_files
        assert file3 in all_files  # This assertion will fail with current implementation
