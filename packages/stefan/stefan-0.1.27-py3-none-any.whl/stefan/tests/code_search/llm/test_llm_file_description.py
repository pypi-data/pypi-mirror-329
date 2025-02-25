import unittest
from unittest.mock import MagicMock
from stefan.code_search.llm.llm_file_description import FileDescriptionLLMProcessor
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.tests.fixtures.llm_executor import FakeLLMExecutor

class TestFileDescriptionLLMProcessor(unittest.TestCase):
    def setUp(self):
        # Create a mock LLMExecutor
        self.fake_llm_executor = FakeLLMExecutor()
        
        # Initialize FileDescriptionLLMProcessor with the mock
        self.processor = FileDescriptionLLMProcessor(llm_executor=self.fake_llm_executor)

    def test_extract_public_interface_and_description_success(self):
        # Mock the response from LLMExecutor
        mock_response = "<public_interface>MyClass</public_interface><description>Description</description>"
        self.fake_llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, mock_response)
        
        # Define test inputs
        file_content = "class MyClass"
        file_path = "test_file.py"
        
        # Call the method under test
        response = self.processor.extract_public_interface_and_description(
            file_content=file_content,
            file_path=file_path,
        )
        
        # Assert the expected result
        self.assertEqual(response.public_interface, "MyClass")
        self.assertEqual(response.description, "Description")

        # Assert LLM was called
        self.fake_llm_executor.assert_records_count_total(1)

    def test_extract_public_interface_and_description_no_description(self):
        # Mock the response from LLMExecutor
        mock_response = "<public_interface>MyClass</public_interface>>"
        self.fake_llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, mock_response)
        
        # Define test inputs
        file_content = "class MyClass"
        file_path = "test_file.py"
        
        # Call the method under test and assert it raises a ValueError
        with self.assertRaises(ValueError):
            self.processor.extract_public_interface_and_description(file_content, file_path)
            
    def test_extract_public_interface_and_description_no_public_interface(self):
        # Mock the response from LLMExecutor
        mock_response = "<description>Description</description>"
        self.fake_llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, mock_response)
        
        # Define test inputs
        file_content = "class MyClass"
        file_path = "test_file.py"
        
        # Call the method under test and assert it raises a ValueError
        with self.assertRaises(ValueError):
            self.processor.extract_public_interface_and_description(file_content, file_path)
