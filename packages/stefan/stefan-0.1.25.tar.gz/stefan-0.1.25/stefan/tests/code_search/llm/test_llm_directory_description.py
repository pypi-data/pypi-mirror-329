import unittest
from datetime import datetime
from stefan.code_search.llm.llm_directory_description import DirectoryDescriptionLLMProcessor
from stefan.code_search.file_system_nodes import DirectoryNode, FileNode
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.tests.fixtures.llm_executor import FakeLLMExecutor

class TestDirectoryDescriptionLLMProcessor(unittest.TestCase):
    def setUp(self):
        self.fake_llm_executor = FakeLLMExecutor()
        self.processor = DirectoryDescriptionLLMProcessor(llm_executor=self.fake_llm_executor)

    def test_extract_directory_description_success(self):
        # Create mock directory structure
        mock_file = FileNode(
            name="test.py",
            path="/test/test.py",
            last_modified=datetime.now(),
            description="A test file description",
            file_size=100,
            file_hash="hash",
        )
        mock_subdir = DirectoryNode(
            name="subdir",
            path="/test/subdir",
            last_modified=datetime.now(),
            description="A test subdirectory description",
            children=[],
        )
        mock_directory = DirectoryNode(
            name="test",
            path="/test",
            last_modified=datetime.now(),
            description=None,
            children=[mock_subdir, mock_file],
        )

        # Mock the response from LLMExecutor
        mock_response = "<description>Description</description>"
        self.fake_llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, mock_response)
        
        # Call the method under test
        result = self.processor.extract_directory_description(mock_directory)
        
        # Assert the expected result
        self.assertEqual(result.description, "Description")
        self.fake_llm_executor.assert_records_count_total(1)

    def test_extract_directory_description_missing_file_description(self):
        # Create mock directory structure with missing file description
        mock_file = FileNode(
            name="test.py",
            path="/test/test.py",
            last_modified=datetime.now(),
            description=None,  # Missing description
            file_size=100,
            file_hash="hash",
        )
        mock_directory = DirectoryNode(
            name="test",
            path="/test",
            last_modified=datetime.now(),
            description="Description",
            children=[mock_file],
            directories=[],
        )
        
        # Call the method under test and assert it raises a ValueError
        with self.assertRaises(ValueError) as context:
            self.processor.extract_directory_description(mock_directory)

    def test_extract_directory_description_missing_subdir_description(self):
        # Create mock directory structure with missing subdirectory description
        mock_subdir = DirectoryNode(
            name="subdir",
            path="/test/subdir",
            last_modified=datetime.now(),
            description="Description",
        )
        mock_directory = DirectoryNode(
            name="test",
            path="/test",
            last_modified=datetime.now(),
            children=[],
            directories=[mock_subdir],
            description=None,
        )
        
        # Call the method under test and assert it raises a ValueError
        with self.assertRaises(ValueError) as context:
            self.processor.extract_directory_description(mock_directory)

    def test_extract_directory_description_invalid_response(self):
        # Create mock directory structure
        mock_directory = DirectoryNode(
            name="test",
            path="/test",
            last_modified=datetime.now(),
            children=[],
            directories=[]
        )

        # Mock an invalid response from LLMExecutor (missing description tags)
        mock_response = "Invalid response without XML tags"
        self.fake_llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, mock_response)
        
        # Call the method under test and assert it raises a ValueError
        with self.assertRaises(ValueError) as context:
            self.processor.extract_directory_description(mock_directory)
