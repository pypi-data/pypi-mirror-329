from datetime import datetime
import unittest
from unittest.mock import MagicMock, mock_open, patch
from stefan.code_search.llm.llm_file_relevancy import FileRelevancyLLMProcessor, FileRelevancyResult
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.code_search.file_system_nodes import FileNode
from stefan.tests.fixtures.llm_executor import FakeLLMExecutor
from stefan.utils.async_execution import FakeAsyncExecution

class TestFileRelevancyProcessor(unittest.TestCase):
    def setUp(self):
        self.context = ExecutionContext.empty()
        self.fake_llm_executor = FakeLLMExecutor()
        self.processor = FileRelevancyLLMProcessor(
            llm_executor=self.fake_llm_executor,
            async_execution=FakeAsyncExecution()
        )

    def test_determine_relevancy_success(self):
        mock_response = """
        <answer>
        <reasoning>This file is relevant because it contains the search functionality.</reasoning>
        <score>0.85</score>
        <is_relevant>true</is_relevant>
        </answer>
        """
        self.fake_llm_executor.add_response(LLMTag.CODE_SEARCH_FILE_RELEVANCY, mock_response)
        
        query = "search query"
        file_nodes = [
            FileNode(
                name="test_file.py",
                path="test_file.py",
                last_modified=datetime.now(),
                file_size=100,
                file_hash="hash",
            ),
        ]
        
        # Mock the file content
        with patch("builtins.open", mock_open(read_data="class MyClass")):
            results = self.processor.determine_relevancy(query, file_nodes, self.context)
        
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertTrue(result.is_relevant)
        self.assertEqual(result.relevance_score, 0.85)
        self.assertEqual(result.explanation, "This file is relevant because it contains the search functionality.")
        self.assertEqual(result.file_path.name, "test_file.py")
        self.fake_llm_executor.assert_records_count_total(1)

    def test_determine_relevancy_invalid_format(self):
        mock_response = "<answer>Invalid format</answer>"
        self.fake_llm_executor.add_response(LLMTag.CODE_SEARCH_FILE_RELEVANCY, mock_response)
        
        query = "search query"
        file_nodes = [
            FileNode(
                name="first.py",
                path="first.py",
                last_modified=datetime.now(),
                file_size=100,
                file_hash="hash",
            ),
        ]
        
        with patch("builtins.open", mock_open(read_data="class MyClass")):
            with self.assertRaises(ValueError):
                self.processor.determine_relevancy(query, file_nodes, self.context)
        
        self.fake_llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_RELEVANCY, 1)

    def test_determine_relevancy_multiple_files(self):
        mock_responses = [
            """
            <answer>
            <reasoning>First file is relevant</reasoning>
            <score>0.9</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Second file is not relevant</reasoning>
            <score>0.2</score>
            <is_relevant>false</is_relevant>
            </answer>
            """
        ]
        self.fake_llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, mock_responses)
        
        query = "search query"
        file_nodes = [
            FileNode(
                name="first.py",
                path="first.py",
                last_modified=datetime.now(),
                file_size=100,
                file_hash="hash",
            ),
            FileNode(
                name="second.py",
                path="second.py",
                last_modified=datetime.now(),
                file_size=100,
                file_hash="hash",
            ),
        ]
        
        with patch("builtins.open", mock_open(read_data="class MyClass")):
            results = self.processor.determine_relevancy(query, file_nodes, self.context)
        
        self.assertEqual(len(results), 2)
        self.assertTrue(results[0].is_relevant)
        self.assertEqual(results[0].relevance_score, 0.9)
        self.assertFalse(results[1].is_relevant)
        self.assertEqual(results[1].relevance_score, 0.2)
        self.fake_llm_executor.assert_records_count_total(2)
