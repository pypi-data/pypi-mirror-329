import pytest
from pathlib import Path
import tempfile

from stefan.code_search.code_search_full_text_with_relevancy import CodeSearchFullTextWithRelevancy
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.llm.llm_file_relevancy import FileRelevancyLLMProcessor
from stefan.execution_context import ExecutionContext
from stefan.project_configuration import ProjectContext
from stefan.tests.fixtures.dummy_project_context import create_dummy_project_context
from stefan.tests.fixtures.llm_executor import FakeLLMExecutor
from stefan.utils.async_execution import FakeAsyncExecution
from stefan.code_search.llm.llm_tag import LLMTag

class TestCodeSearchFullTextWithRelevancy:
    @pytest.fixture
    def execution_context(self):
        return ExecutionContext.empty()

    @pytest.fixture
    def temp_directory(self):
        """Create a temporary directory structure for testing"""
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            
            # Create directories
            (root / "dir1").mkdir()
            (root / "dir2").mkdir()
            
            # Create Python files with specific content for full-text search
            (root / "file1.py").write_text("def search_function(): return 'XXX content'")
            (root / "dir1" / "file2.py").write_text("class SearchClass:\n    XXX_term = 'findable'")
            (root / "dir2" / "file3.py").write_text("NO TERMS HERE - THIS FILE SHOULD NOT BE RETURNED BY FULLTEXT")
            
            yield root

    @pytest.fixture
    def llm_executor(self):
        return FakeLLMExecutor()

    @pytest.fixture
    def code_search(self, temp_directory, llm_executor):
        project_context = create_dummy_project_context(
            path=str(temp_directory),
            include_patterns=["*.py"],
            exclude_patterns=[".git", "__pycache__"]
        )

        tree_builder = CodeSearchTreeCreator(
            project_context=project_context,
        )
        file_relevancy_processor = FileRelevancyLLMProcessor(
            llm_executor=llm_executor,
            async_execution=FakeAsyncExecution(),
        )
        
        return CodeSearchFullTextWithRelevancy(
            tree_builder=tree_builder,
            llm_file_relevancy=file_relevancy_processor,
            project_context=project_context,
        )

    def test_perform_search_finds_relevant_files(
        self,
        code_search: CodeSearchFullTextWithRelevancy,
        llm_executor: FakeLLMExecutor,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test that search finds files containing search text and ranks them by relevance"""
        # Set up relevancy responses
        relevancy_responses = [
            """
            <answer>
            <reasoning>Highly relevant search function</reasoning>
            <score>0.9</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Somewhat relevant search class</reasoning>
            <score>0.6</score>
            <is_relevant>true</is_relevant>
            </answer>
            """
        ]
        llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_responses)
        
        # Perform search
        results = code_search.perform_search_fulltext_with_relevancy(
            fulltext_search_query="XXX",
            llm_query="Find search related functionality",
            context=execution_context
        )
        
        # Verify results
        assert len(results) == 2
        assert results[0].file_path == temp_directory / "file1.py"
        assert results[1].file_path == temp_directory / "dir1" / "file2.py"
        
        # Verify scores and explanations
        assert results[0].relevance_score == 0.9
        assert results[0].explanation == "Highly relevant search function"
        assert results[1].relevance_score == 0.6
        assert results[1].explanation == "Somewhat relevant search class"

    def test_perform_search_with_no_text_matches(
        self,
        code_search: CodeSearchFullTextWithRelevancy,
        llm_executor: FakeLLMExecutor,
        execution_context: ExecutionContext
    ):
        """Test search when no files contain the search text"""
        results = code_search.perform_search_fulltext_with_relevancy(
            fulltext_search_query="nonexistent_term",
            llm_query="Find nonexistent functionality",
            context=execution_context
        )
        
        assert len(results) == 0
        # Verify no relevancy calls were made since no files matched
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_RELEVANCY, 0)

    def test_perform_search_with_text_match_but_no_relevance(
        self,
        code_search: CodeSearchFullTextWithRelevancy,
        llm_executor: FakeLLMExecutor,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test search when files contain search text but are not relevant"""
        # Set up relevancy responses indicating no relevance
        relevancy_responses = [
            """
            <answer>
            <reasoning>Not relevant despite text match</reasoning>
            <score>0.2</score>
            <is_relevant>false</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Also not relevant</reasoning>
            <score>0.1</score>
            <is_relevant>false</is_relevant>
            </answer>
            """
        ]
        llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_responses)
        
        results = code_search.perform_search_fulltext_with_relevancy(
            fulltext_search_query="XXX",
            llm_query="Find completely unrelated functionality",
            context=execution_context
        )
        
        assert len(results) == 0

    def test_perform_search_respects_file_patterns(
        self,
        code_search: CodeSearchFullTextWithRelevancy,
        temp_directory: Path,
        llm_executor: FakeLLMExecutor,
        execution_context: ExecutionContext
    ):
        """Test that search only includes files matching the include patterns"""
        # Create both Python and text files with same content
        (temp_directory / "test.py").write_text("XXYYXX content")
        (temp_directory / "test.txt").write_text("XXYYXX content")
        
        relevancy_response = """
        <answer>
        <reasoning>Relevant Python file</reasoning>
        <score>0.8</score>
        <is_relevant>true</is_relevant>
        </answer>
        """
        llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_response)
        
        results = code_search.perform_search_fulltext_with_relevancy(
            fulltext_search_query="XXYYXX",
            llm_query="Find test files",
            context=execution_context
        )
        
        # Should only find the Python file
        assert len(results) == 1
        assert results[0].file_path == temp_directory / "test.py"
        assert results[0].relevance_score == 0.8
