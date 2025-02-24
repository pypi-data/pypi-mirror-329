import pytest
from pathlib import Path
import tempfile
import time
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.file_system_nodes import FileSystemNode, DirectoryNode, FileNode, FileSystemTree
from stefan.tests.fixtures.dummy_project_context import create_dummy_project_context

class TestCodeSearch:
    @pytest.fixture
    def temp_directory(self):
        """Create a temporary directory structure for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test directory structure
            root = Path(temp_dir)
            
            # Create some directories
            (root / "dir1").mkdir()
            (root / "dir1" / "subdir").mkdir()
            (root / "dir2").mkdir()
            
            # Create some files
            (root / "file1.py").write_text("content1")
            (root / "dir1" / "file2.py").write_text("content2")
            (root / "dir1" / "subdir" / "file3.py").write_text("content3")
            (root / "dir2" / "file4.txt").write_text("content4")
            (root / ".git").mkdir()
            (root / ".git" / "config").write_text("git config")
            
            yield root

    @pytest.fixture
    def code_search(self, temp_directory):
        project_context = create_dummy_project_context(
            path=str(temp_directory),
            include_patterns=["*.py", "*.txt"],
            exclude_patterns=[".git", "__pycache__"]
        )
        return CodeSearchTreeCreator(
            project_context=project_context,
        )

    def test_build_file_tree_structure(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that the file tree is built with correct structure"""
        tree = code_search.build_file_tree(temp_directory)
        
        assert isinstance(tree, FileSystemTree)
        assert tree.root.name == temp_directory.name
        
        # Check if we have correct number of top-level items (excluding .git)
        top_level = [child for child in tree.root.children if not child.name.startswith('.')]
        assert len(top_level) == 3  # file1.py, dir1, dir2
        
        # Find dir1 and check its contents
        dir1 = next(child for child in tree.root.children if child.name == "dir1")
        assert isinstance(dir1, DirectoryNode)
        assert len(dir1.children) == 2  # file2.py and subdir

    def test_build_file_tree_exclusions(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that excluded patterns are properly handled"""
        tree = code_search.build_file_tree(temp_directory)
        
        # Check that .git directory is excluded
        git_dirs = [child for child in tree.root.children if child.name == ".git"]
        assert len(git_dirs) == 0

    def test_build_file_tree_inclusions(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that include patterns are properly handled"""
        # Only include .py files
        tree = code_search.build_file_tree(temp_directory, include_patterns=["*.py"])
        
        # Recursively collect all file names
        def collect_files(node: FileSystemNode):
            files = []
            if isinstance(node, DirectoryNode):
                for child in node.children:
                    files.extend(collect_files(child))
            else:
                files.append(node.name)
            return files
        
        files = collect_files(tree.root)
        assert all(f.endswith('.py') for f in files)
        assert not any(f.endswith('.txt') for f in files)

    def test_compare_trees_no_changes(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test comparison of identical trees"""
        tree1 = code_search.build_file_tree(temp_directory)
        tree2 = code_search.build_file_tree(temp_directory)
        
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Verify no nodes are marked for recalculation
        def verify_no_recalculation(node: FileSystemNode):
            assert not node.should_be_recalculated
            if isinstance(node, DirectoryNode):
                for child in node.children:
                    verify_no_recalculation(child)
        
        verify_no_recalculation(tree2.root)

    def test_compare_trees_with_modifications(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test detection of modified files"""
        # Build initial tree
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Modify a file
        test_file = temp_directory / "file1.py"
        time.sleep(0.1)  # Ensure modification time is different
        test_file.write_text("modified content")
        
        # Build new tree
        tree2 = code_search.build_file_tree(temp_directory)
        
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Find the modified file node
        modified_file = next(
            child for child in tree2.root.children 
            if isinstance(child, FileNode) and child.name == "file1.py"
        )

        # Verify modified file and its parent are marked for recalculation
        assert modified_file.should_be_recalculated
        assert tree2.root.should_be_recalculated

    def test_compare_trees_with_additions(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test detection of added files"""
        # Build initial tree
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Add a new file
        new_file = temp_directory / "dir1" / "new_file.py"
        new_file.write_text("new content")
        
        # Build new tree
        tree2 = code_search.build_file_tree(temp_directory)
        
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Find dir1 and the new file
        dir1 = next(child for child in tree2.root.children if child.name == "dir1")
        new_file_node = next(child for child in dir1.children if child.name == "new_file.py")
        
        # Verify new file and its parent directories are marked for recalculation
        assert new_file_node.should_be_recalculated
        assert dir1.should_be_recalculated
        assert tree2.root.should_be_recalculated

    def test_compare_trees_with_removals(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test detection of removed files"""
        # Build initial tree
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Remove a file
        file_to_remove = temp_directory / "file1.py"
        file_to_remove.unlink()
        
        # Build new tree
        tree2 = code_search.build_file_tree(temp_directory)
        
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Root should be marked for recalculation since a file was removed
        assert tree2.root.should_be_recalculated is True
        
        # Verify that unaffected directories are not marked for recalculation
        dir1 = next(child for child in tree2.root.children if child.name == "dir1")
        assert dir1.should_be_recalculated is False

    def test_compare_trees_with_directory_removal(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test recalculation flags when removing directories"""
        # Build initial tree
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Remove an entire directory
        dir_to_remove = temp_directory / "dir1"
        # First remove all files
        for item in dir_to_remove.rglob('*'):
            if item.is_file():
                item.unlink()
        # Then remove all directories from deepest to root
        for item in sorted(dir_to_remove.rglob('*'), key=lambda x: len(str(x.resolve()).split('/')), reverse=True):
            if item.is_dir():
                item.rmdir()
        dir_to_remove.rmdir()
        
        # Build new tree
        tree2 = code_search.build_file_tree(temp_directory)
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Root should be recalculated since a directory was removed
        assert tree2.root.should_be_recalculated is True
        
        # dir2 should not be recalculated as it wasn't affected
        dir2 = next(child for child in tree2.root.children if child.name == "dir2")
        assert dir2.should_be_recalculated is False

    def test_recalculation_flags_no_changes(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that recalculation flags are False when no changes"""
        tree1 = code_search.build_file_tree(temp_directory)
        tree2 = code_search.build_file_tree(temp_directory)
        
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        def check_flags(node: FileSystemNode):
            assert node.should_be_recalculated is False
            if isinstance(node, DirectoryNode):
                for child in node.children:
                    check_flags(child)
        
        check_flags(tree2.root)

    def test_recalculation_flags_with_modification(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that recalculation flags are properly set when file is modified"""
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Modify a file
        test_file = temp_directory / "dir1" / "file2.py"
        time.sleep(0.1)
        test_file.write_text("modified content")
        
        tree2 = code_search.build_file_tree(temp_directory)
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Find the modified file node and its parent directories
        modified_file = None
        dir1 = None
        root = tree2.root
        
        for child in root.children:
            if child.name == "dir1":
                dir1 = child
                for file in child.children:
                    if file.name == "file2.py":
                        modified_file = file
                        break
                break
        
        assert modified_file.should_be_recalculated is True
        assert dir1.should_be_recalculated is True
        assert root.should_be_recalculated is True

    def test_recalculation_flags_with_new_file(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that recalculation flags are properly set when new file is added"""
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Add new file
        new_file = temp_directory / "dir1" / "new_file.py"
        new_file.write_text("new content")
        
        tree2 = code_search.build_file_tree(temp_directory)
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Find dir1 and the new file
        dir1 = next(child for child in tree2.root.children if child.name == "dir1")
        new_file_node = next(child for child in dir1.children if child.name == "new_file.py")
        
        assert new_file_node.should_be_recalculated is True
        assert dir1.should_be_recalculated is True
        assert tree2.root.should_be_recalculated is True
        
        # Other directories should be false
        dir2 = next(child for child in tree2.root.children if child.name == "dir2")
        assert dir2.should_be_recalculated is False

    def test_recalculation_flags_with_nested_changes(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test recalculation flags with nested directory changes"""
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Modify a deeply nested file
        nested_file = temp_directory / "dir1" / "subdir" / "file3.py"
        time.sleep(0.1)
        nested_file.write_text("modified nested content")
        
        tree2 = code_search.build_file_tree(temp_directory)
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Find all relevant nodes
        dir1 = next(child for child in tree2.root.children if child.name == "dir1")
        subdir = next(child for child in dir1.children if child.name == "subdir")
        modified_file = next(child for child in subdir.children if child.name == "file3.py")
        
        # Check recalculation flags propagate up the tree
        assert modified_file.should_be_recalculated is True
        assert subdir.should_be_recalculated is True
        assert dir1.should_be_recalculated is True
        assert tree2.root.should_be_recalculated is True
        
        # Other paths should not be marked for recalculation
        dir2 = next(child for child in tree2.root.children if child.name == "dir2")
        assert dir2.should_be_recalculated is False

    def test_recalculation_flags_mixed_changes(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test recalculation flags with multiple types of changes"""
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Make multiple changes:
        # 1. Modify a file
        file1 = temp_directory / "file1.py"
        time.sleep(0.1)
        file1.write_text("modified content")
        
        # 2. Add a new file
        new_file = temp_directory / "dir2" / "new_file.py"
        new_file.write_text("new content")
        
        # 3. Remove a file
        remove_file = temp_directory / "dir1" / "file2.py"
        remove_file.unlink()
        
        tree2 = code_search.build_file_tree(temp_directory)
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Root should be recalculated
        assert tree2.root.should_be_recalculated is True
        
        # Check modified file
        modified_file = next(child for child in tree2.root.children if child.name == "file1.py")
        assert modified_file.should_be_recalculated is True
        
        # Check directory with new file
        dir2 = next(child for child in tree2.root.children if child.name == "dir2")
        assert dir2.should_be_recalculated is True
        new_file_node = next(child for child in dir2.children if child.name == "new_file.py")
        assert new_file_node.should_be_recalculated is True
        
        # Check directory with removed file
        dir1 = next(child for child in tree2.root.children if child.name == "dir1")
        assert dir1.should_be_recalculated is True

    def test_recalculation_flags_with_file_patterns(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test recalculation flags when using include patterns"""
        # Build initial tree with only .py files
        tree1 = code_search.build_file_tree(temp_directory, include_patterns=["*.py"])
        
        # Modify both .py and .txt files
        py_file = temp_directory / "file1.py"
        txt_file = temp_directory / "dir2" / "file4.txt"
        time.sleep(0.1)
        py_file.write_text("modified py content")
        txt_file.write_text("modified txt content")
        
        tree2 = code_search.build_file_tree(temp_directory, include_patterns=["*.py"])
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Check that only .py file changes affect recalculation flags
        modified_py = next(child for child in tree2.root.children if child.name == "file1.py")
        assert modified_py.should_be_recalculated is True
        
        # dir2 should not be marked for recalculation as the .txt file change was not included
        dir2 = next(child for child in tree2.root.children if child.name == "dir2")
        assert dir2.should_be_recalculated is False

    def test_mark_all_for_recalculation(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that mark_all_for_recalculation properly marks all nodes"""
        # Build tree
        tree = code_search.build_file_tree(temp_directory)
        
        # Initially all nodes should be unmarked
        def verify_no_recalculation(node: FileSystemNode):
            assert not node.should_be_recalculated
            if isinstance(node, DirectoryNode):
                for child in node.children:
                    verify_no_recalculation(child)
        
        verify_no_recalculation(tree.root)
        
        # Mark all nodes for recalculation
        code_search.mark_all_for_recalculation(tree)
        
        # Verify all nodes are now marked
        def verify_all_marked(node: FileSystemNode):
            assert node.should_be_recalculated is True
            if isinstance(node, DirectoryNode):
                for child in node.children:
                    verify_all_marked(child)
        
        verify_all_marked(tree.root)

    def test_directory_recalculation_on_file_modification(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that modifying a file marks its parent directory for recalculation"""
        # Build initial tree
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Modify a file
        test_file = temp_directory / "dir1" / "file2.py"
        time.sleep(0.1)  # Ensure modification time is different
        test_file.write_text("modified content")
        
        # Build new tree
        tree2 = code_search.build_file_tree(temp_directory)
        
        # Compare trees
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Find the modified file node and its parent directory
        dir1 = next(child for child in tree2.root.children if child.name == "dir1")
        modified_file = next(child for child in dir1.children if child.name == "file2.py")
        
        # Verify that the modified file and its parent directory are marked for recalculation
        assert modified_file.should_be_recalculated is True
        assert dir1.should_be_recalculated is True
        assert tree2.root.should_be_recalculated is True

    def test_description_preservation_no_changes(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that descriptions are preserved when no changes occur"""
        # Build initial tree
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Set some descriptions
        test_file = next(child for child in tree1.root.children if isinstance(child, FileNode))
        test_file.description = "Test file description"
        
        dir1 = next(child for child in tree1.root.children if child.name == "dir1")
        dir1.description = "Directory 1 description"
        
        # Build new tree and compare
        tree2 = code_search.build_file_tree(temp_directory)
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Verify descriptions are preserved
        new_test_file = next(child for child in tree2.root.children if isinstance(child, FileNode))
        assert new_test_file.description == "Test file description"
        
        new_dir1 = next(child for child in tree2.root.children if child.name == "dir1")
        assert new_dir1.description == "Directory 1 description"

    def test_description_reset_on_changes(self, code_search: CodeSearchTreeCreator, temp_directory: Path):
        """Test that descriptions are not preserved when changes occur"""
        # Build initial tree
        tree1 = code_search.build_file_tree(temp_directory)
        
        # Set some descriptions
        dir1 = next(child for child in tree1.root.children if child.name == "dir1")
        dir1.description = "Directory 1 description"
        
        file2 = next(child for child in dir1.children if child.name == "file2.py")
        file2.description = "File 2 description"
        
        # Modify a file inside dir1
        file_path = temp_directory / "dir1" / "file2.py"
        time.sleep(0.1)  # Ensure modification time is different
        file_path.write_text("modified content")
        
        # Build new tree and compare
        tree2 = code_search.build_file_tree(temp_directory)
        code_search.compare_trees_and_mark_recalculation(tree1, tree2)
        
        # Find the modified file and its parent directory
        new_dir1 = next(child for child in tree2.root.children if child.name == "dir1")
        new_file2 = next(child for child in new_dir1.children if child.name == "file2.py")
        
        # Verify description is not preserved for modified file
        assert new_file2.description is None
        
        # Verify description is not preserved for parent directory
        assert new_dir1.description is None

    
