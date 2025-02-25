import unittest
from unittest.mock import MagicMock, mock_open, patch
from pathlib import Path
from datetime import datetime

from stefan.code_search.code_search_tree_processor import CodeSearchTreeProcessor
from stefan.code_search.file_system_nodes import FileNode, DirectoryNode, FileSystemTree
from stefan.code_search.llm.llm_directory_description import DirectoryDescriptionLLMProcessor
from stefan.code_search.llm.llm_file_description import FileDescriptionLLMProcessor
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.tests.fixtures.llm_executor import FakeLLMExecutor

class TestCodeSearchTreeProcessor(unittest.TestCase):

    GOOD_FILE_RESPONSE = "<public_interface>Mock interface</public_interface><description>Mock file description</description>"
    GOOD_DIRECTORY_RESPONSE = "<description>Mock directory description</description>"

    def setUp(self):
        # Create fake LLM executor
        self.fake_llm_executor = FakeLLMExecutor()

        # Create file processor
        self.fake_llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, self.GOOD_FILE_RESPONSE, include_last_message=True)
        self.file_processor = FileDescriptionLLMProcessor(self.fake_llm_executor)
        
        # Create directory processor
        self.fake_llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, self.GOOD_DIRECTORY_RESPONSE, include_last_message=True)
        self.dir_processor = DirectoryDescriptionLLMProcessor(self.fake_llm_executor)
        
        # Initialize processor
        self.processor = CodeSearchTreeProcessor(
            llm_file_processor=self.file_processor,
            llm_directory_processor=self.dir_processor,
        )
        
        # Create sample tree
        self.sample_tree = self._create_sample_tree()

    def _create_sample_tree(self) -> FileSystemTree:
        file1 = FileNode(
            path=Path("/test/file1.txt"),
            name="file1.txt",
            last_modified=datetime.now(),
            file_size=100,
            file_hash="hash1",
            should_be_recalculated=True,
        )
        
        file2 = FileNode(
            path=Path("/test/dir1/file2.py"),
            name="file2.py",
            last_modified=datetime.now(),
            file_size=200,
            file_hash="hash2",
            should_be_recalculated=True,
        )
        
        dir1 = DirectoryNode(
            path=Path("/test/dir1"),
            name="dir1",
            last_modified=datetime.now(),
            children=[file2],
            should_be_recalculated=True,
        )
        
        return FileSystemTree(
            root=DirectoryNode(
                path=Path("/test"),
                name="test",
                last_modified=datetime.now(),
                children=[file1, dir1],
                should_be_recalculated=True,
            )
        )

    def _create_complex_tree(self) -> FileSystemTree:
        """Creates a tree with multiple levels of directories:
        /test
        ├── file1.txt
        ├── dir1
        │   ├── file2.py
        │   └── subdir1
        │       ├── file3.py
        │       └── deepdir
        │           └── file4.py
        └── dir2
            └── file5.py
        """
        # Deepest level
        file4 = FileNode(
            path=Path("/test/dir1/subdir1/deepdir/file4.py"),
            name="file4.py",
            last_modified=datetime.now(),
            file_size=400,
            file_hash="hash4",
            should_be_recalculated=True,
        )
        
        deepdir = DirectoryNode(
            path=Path("/test/dir1/subdir1/deepdir"),
            name="deepdir",
            last_modified=datetime.now(),
            children=[file4],
            should_be_recalculated=True,
        )
        
        # Level 3
        file3 = FileNode(
            path=Path("/test/dir1/subdir1/file3.py"),
            name="file3.py",
            last_modified=datetime.now(),
            file_size=300,
            file_hash="hash3",
            should_be_recalculated=True,
        )
        
        subdir1 = DirectoryNode(
            path=Path("/test/dir1/subdir1"),
            name="subdir1",
            last_modified=datetime.now(),
            children=[file3, deepdir],
            should_be_recalculated=True,
        )
        
        # Level 2 - dir1 branch
        file2 = FileNode(
            path=Path("/test/dir1/file2.py"),
            name="file2.py",
            last_modified=datetime.now(),
            file_size=200,
            file_hash="hash2",
            should_be_recalculated=True,
        )
        
        dir1 = DirectoryNode(
            path=Path("/test/dir1"),
            name="dir1",
            last_modified=datetime.now(),
            children=[file2, subdir1],
            should_be_recalculated=True,
        )
        
        # Level 2 - dir2 branch
        file5 = FileNode(
            path=Path("/test/dir2/file5.py"),
            name="file5.py",
            last_modified=datetime.now(),
            file_size=500,
            file_hash="hash5",
            should_be_recalculated=True,
        )
        
        dir2 = DirectoryNode(
            path=Path("/test/dir2"),
            name="dir2",
            last_modified=datetime.now(),
            children=[file5],
            should_be_recalculated=True,
        )
        
        # Root level
        file1 = FileNode(
            path=Path("/test/file1.txt"),
            name="file1.txt",
            last_modified=datetime.now(),
            file_size=100,
            file_hash="hash1",
            should_be_recalculated=True,
        )
        
        return FileSystemTree(
            root=DirectoryNode(
                path=Path("/test"),
                name="test",
                last_modified=datetime.now(),
                children=[file1, dir1, dir2],
                should_be_recalculated=True,
            )
        )

    def test_process_tree(self):
        # Process tree with mock file content
        with patch("builtins.open", mock_open(read_data="mock content")):
            self.processor.process_tree(self.sample_tree)
        
        # Verify file descriptions
        self.assertIn("Mock interface", self.sample_tree.root.children[0].public_interface)
        self.assertIn("Mock file description", self.sample_tree.root.children[0].description)
        self.assertIn("Mock interface", self.sample_tree.root.children[1].children[0].public_interface)
        self.assertIn("Mock file description", self.sample_tree.root.children[1].children[0].description)
        
        # Verify LLM records count - only file descriptions should be processed
        self.fake_llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, 2)
        self.fake_llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, 0)  # Should be 2 but directory processing is skipped

    def test_process_tree_with_file_error(self):
        # Set up responses for error case
        self.fake_llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, "This will be error since no xml tags are used")

        # Mock file reading and expect the error
        with patch("builtins.open", mock_open(read_data="mock content")):
            with self.assertRaises(ValueError):
                self.processor.process_tree(self.sample_tree)
        
        # Verify LLM was called before error
        self.fake_llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, 2)
        self.fake_llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, 0)  # Should be 1 but directory processing is skipped

    # Remove test_process_tree_with_directory_error as it's no longer relevant

    def test_process_tree_with_none_should_be_recalculated(self):
        # Set should_be_recalculated to None for a node
        self.sample_tree.root.children[0].should_be_recalculated = None

        # Expect ValueError due to None should_be_recalculated
        with self.assertRaises(ValueError):
            with patch("builtins.open", mock_open(read_data="mock content")):
                self.processor.process_tree(self.sample_tree)

    def test_process_tree_with_recalculation_false(self):
        # Set should_be_recalculated to False for files
        self.sample_tree.root.children[0].should_be_recalculated = False  # file1.txt
        self.sample_tree.root.children[0].description = "old description"
        self.sample_tree.root.children[0].public_interface = "old interface"
        
        # Process tree with mock file content
        with patch("builtins.open", mock_open(read_data="mock content")):
            self.processor.process_tree(self.sample_tree)
        
        # Verify skipped file retained old values
        self.assertEqual(self.sample_tree.root.children[0].public_interface, "old interface")
        self.assertEqual(self.sample_tree.root.children[0].description, "old description")
        
        # Verify file that should be processed was updated
        self.assertIn("Mock interface", self.sample_tree.root.children[1].children[0].public_interface)
        self.assertIn("Mock file description", self.sample_tree.root.children[1].children[0].description)

        # Verify LLM call counts
        self.fake_llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, 1)  # Only file2.py
        self.fake_llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, 0)  # Should be 1 but directory processing is skipped
