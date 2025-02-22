import pytest
from pathlib import Path
import tempfile
import time

from stefan.code_search.code_search_relevancy import CodeSearchRelevancy
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.code_search_tree_processor import CodeSearchTreeProcessor
from stefan.code_search.code_search_persistence import CodeSearchPersistence
from stefan.code_search.llm.llm_file_relevancy import FileRelevancyLLMProcessor
from stefan.code_search.llm.llm_file_description import FileDescriptionLLMProcessor
from stefan.code_search.llm.llm_directory_description import DirectoryDescriptionLLMProcessor
from stefan.execution_context import ExecutionContext
from stefan.code_search.llm.llm_tag import LLMTag
from stefan.project_configuration import STEFAN_OUTPUTS_DIRECTORY, ProjectContext
from stefan.tests.fixtures.dummy_project_context import create_dummy_project_context
from stefan.tests.fixtures.llm_executor import FakeLLMExecutor
from stefan.utils.async_execution import FakeAsyncExecution

class TestCodeSearch:
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
            (root / "dir1" / "subdir").mkdir()
            (root / "dir2").mkdir()
            
            # Create Python files with content
            (root / "file1.py").write_text("def function1(): pass")
            (root / "dir1" / "file2.py").write_text("class Class2: pass")
            (root / "dir1" / "subdir" / "file3.py").write_text("def function3(): pass")
            
            # Create non-Python file
            (root / "dir2" / "file4.txt").write_text("text content")
            
            yield root

    @pytest.fixture
    def llm_executor(self):
        """Create fake LLM executors for different processors"""
        fake_llm_executor = FakeLLMExecutor()
        
        # Set up responses for file description
        fake_llm_executor.set_fixed_response(
            LLMTag.CODE_SEARCH_FILE_DESCRIPTION,
            "<public_interface>public interface</public_interface><description>file description</description>"
        )
        
        # Set up responses for directory description
        fake_llm_executor.set_fixed_response(
            LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION,
            "<description>directory description</description>"
        )
        
        return fake_llm_executor

    @pytest.fixture
    def code_search(self, temp_directory, llm_executor: FakeLLMExecutor):
        """Create CodeSearch instance with real implementations"""
        # Create processors with fake executors
        file_desc_processor = FileDescriptionLLMProcessor(llm_executor)
        dir_desc_processor = DirectoryDescriptionLLMProcessor(llm_executor)
        file_relevancy_processor = FileRelevancyLLMProcessor(llm_executor, FakeAsyncExecution())
        
        # Create real implementations
        tree_processor = CodeSearchTreeProcessor(
            llm_file_processor=file_desc_processor,
            llm_directory_processor=dir_desc_processor,
        )
        persistence = CodeSearchPersistence()
        
        # Create project context
        project_context = create_dummy_project_context(
            path=str(temp_directory),
            include_patterns=["*.py"],
            exclude_patterns=[".git", "__pycache__"]
        )

        tree_builder = CodeSearchTreeCreator(
            project_context=project_context,
        )
        
        return CodeSearchRelevancy(
            tree_processor=tree_processor,
            tree_builder=tree_builder,
            llm_file_relevancy=file_relevancy_processor,
            persistence=persistence,
            project_context=project_context,
        )

    def test_perform_search_finds_relevant_files(
        self,
        code_search: CodeSearchRelevancy,
        llm_executor: FakeLLMExecutor,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test that search finds and ranks relevant files correctly"""
        # Set up relevancy responses for the three Python files
        relevancy_responses = [
            """
            <answer>
            <reasoning>Highly relevant main file</reasoning>
            <score>0.9</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Somewhat relevant class file</reasoning>
            <score>0.7</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Not very relevant function</reasoning>
            <score>0.3</score>
            <is_relevant>false</is_relevant>
            </answer>
            """
        ]
        llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_responses)
        
        # Perform search
        results = code_search.perform_search_with_query(
            query="find main function",
            max_files=5,
            select_all_high_relevant_files=True,
            context=execution_context
        )
        
        # Verify results
        assert len(results) == 2  # Only two files should be relevant
        assert results[0].file_path == temp_directory / "file1.py"  # Highest score should be first
        assert results[1].file_path == temp_directory / "dir1" / "file2.py"
        
        # Verify result properties
        assert results[0].file_description == "file description"
        assert results[0].file_public_interface == "public interface"
        assert results[0].relevance_score == 0.9
        assert results[0].explanation == "Highly relevant main file"
        
        # Verify LLM calls
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, 3)       # Three Python files processed
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, 0)  # Should be 2 (Root + two directories) but directory processing is skipped
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_RELEVANCY, 3)         # Three files evaluated
        llm_executor.assert_records_count_total(6)

    def test_perform_search_with_no_relevant_files(
        self,
        code_search: CodeSearchRelevancy,
        llm_executor: FakeLLMExecutor,
        execution_context: ExecutionContext
    ):
        """Test search when no files are relevant to the query"""
        # Set up relevancy responses indicating no relevant files
        relevancy_responses = [
            """
            <answer>
            <reasoning>Not relevant</reasoning>
            <score>0.2</score>
            <is_relevant>false</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Not relevant</reasoning>
            <score>0.1</score>
            <is_relevant>false</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Not relevant</reasoning>
            <score>0.15</score>
            <is_relevant>false</is_relevant>
            </answer>
            """
        ]
        llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_responses)
        
        # Perform search
        results = code_search.perform_search_with_query(
            query="completely unrelated query",
            max_files=5,
            select_all_high_relevant_files=True,
            context=execution_context
        )
        
        # Verify results
        assert len(results) == 0
        
        # Verify LLM calls
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, 3)
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, 0) # Should be 4 but directory processing is skipped
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_RELEVANCY, 3)

    def test_perform_search_with_tree_persistence(
        self,
        code_search: CodeSearchRelevancy,
        llm_executor: FakeLLMExecutor,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test that tree is properly persisted and reused"""
        # Set up initial relevancy response
        initial_response = """
        <answer>
            <reasoning>Relevant file</reasoning>
            <score>0.8</score>
            <is_relevant>true</is_relevant>
        </answer>
        """
        llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_RELEVANCY, initial_response)
        
        # First search to create and persist tree
        code_search.perform_search_with_query(
            query="initial query",
            max_files=5,
            select_all_high_relevant_files=True,
            context=execution_context
        )
        
        # Verify tree file was created
        tree_file = temp_directory / STEFAN_OUTPUTS_DIRECTORY / "code_search_tree.json"
        assert tree_file.exists()
        
        # Modify a file to test tree comparison
        test_file = temp_directory / "file1.py"
        time.sleep(0.1)  # Ensure modification time is different
        test_file.write_text("def modified_function(): pass")
        
        # Set up new relevancy response
        new_response = """
        <answer>
            <reasoning>Modified file is relevant</reasoning>
            <score>0.95</score>
            <is_relevant>true</is_relevant>
        </answer>
        """
        llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_RELEVANCY, new_response)
        
        # Perform second search
        results = code_search.perform_search_with_query(
            query="find modified function",
            max_files=5,
            select_all_high_relevant_files=True,
            context=execution_context
        )
        
        # Verify results reflect the modified file
        assert len(results) == 3  # All files were returned
        assert results[0].file_path == test_file
        
        # Verify result properties
        assert results[0].file_description == "file description"
        assert results[0].file_public_interface == "public interface"
        assert results[0].relevance_score == 0.95
        assert results[0].explanation == "Modified file is relevant"
        
        # Verify LLM calls
        # First search: 3 files + 3 directories
        # Second search: Only the modified file should be reprocessed
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_DESCRIPTION, 4)  # 3 initial + 1 modified
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_DIRECTORY_DESCRIPTION, 0)  # Should be 6 (3 initial + 3 reprocessed) but directory processing is skipped
        llm_executor.assert_records_count_for_tag(LLMTag.CODE_SEARCH_FILE_RELEVANCY, 6)  # 3 initial + 3 second search

    def test_perform_search_with_invalid_llm_response(
        self,
        code_search: CodeSearchRelevancy,
        llm_executor: FakeLLMExecutor,
        execution_context: ExecutionContext
    ):
        """Test handling of invalid LLM responses"""
        # Set up invalid response
        llm_executor.set_fixed_response(LLMTag.CODE_SEARCH_FILE_RELEVANCY, "Invalid response without XML tags")
        
        # Expect error when performing search
        with pytest.raises(ValueError):
            code_search.perform_search_with_query(
                query="test query",
                max_files=5,
                select_all_high_relevant_files=True,
                context=execution_context
            )

    def test_select_relevant_files_with_high_relevance_override(
        self,
        code_search: CodeSearchRelevancy,
        llm_executor: FakeLLMExecutor,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test that select_all_high_relevant_files=True includes all high relevance files"""
        relevancy_responses = [
            """
            <answer>
            <reasoning>Highly relevant main file</reasoning>
            <score>0.9</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Also highly relevant class file</reasoning>
            <score>0.85</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Less relevant function</reasoning>
            <score>0.7</score>
            <is_relevant>true</is_relevant>
            </answer>
            """
        ]
        llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_responses)
        
        # Perform search with max_files=1 but select_all_high_relevant_files=True
        results = code_search.perform_search_with_query(
            query="find main function",
            max_files=1,
            select_all_high_relevant_files=True,
            context=execution_context
        )
        
        # Verify results - should get both high relevance files despite max_files=1
        assert len(results) == 2
        assert results[0].relevance_score == 0.9
        assert results[1].relevance_score == 0.85

    def test_select_relevant_files_without_high_relevance_override(
        self,
        code_search: CodeSearchRelevancy,
        llm_executor: FakeLLMExecutor,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test that select_all_high_relevant_files=False respects max_files even for high relevance"""
        relevancy_responses = [
            """
            <answer>
            <reasoning>Highly relevant main file</reasoning>
            <score>0.9</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Also highly relevant class file</reasoning>
            <score>0.85</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Less relevant function</reasoning>
            <score>0.7</score>
            <is_relevant>true</is_relevant>
            </answer>
            """
        ]
        llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_responses)
        
        # Perform search with max_files=1 and select_all_high_relevant_files=False
        results = code_search.perform_search_with_query(
            query="find main function",
            max_files=1,
            select_all_high_relevant_files=False,
            context=execution_context
        )
        
        # Verify results - should only get one file despite multiple high relevance files
        assert len(results) == 1
        assert results[0].relevance_score == 0.9

    def test_select_relevant_files_with_no_high_relevance(
        self,
        code_search: CodeSearchRelevancy,
        llm_executor: FakeLLMExecutor,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test behavior when no files have high relevance scores"""
        relevancy_responses = [
            """
            <answer>
            <reasoning>Medium relevance file</reasoning>
            <score>0.7</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Another medium relevance file</reasoning>
            <score>0.6</score>
            <is_relevant>true</is_relevant>
            </answer>
            """,
            """
            <answer>
            <reasoning>Low relevance file</reasoning>
            <score>0.5</score>
            <is_relevant>true</is_relevant>
            </answer>
            """
        ]
        llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_responses)
        llm_executor.add_responses(LLMTag.CODE_SEARCH_FILE_RELEVANCY, relevancy_responses)
        
        # Test with both True and False for select_all_high_relevant_files
        # Should behave the same since no files have high relevance
        for select_all_high_relevant_files in [True, False]:
            results = code_search.perform_search_with_query(
                query="find main function",
                max_files=2,
                select_all_high_relevant_files=select_all_high_relevant_files,
                context=execution_context
            )
            
            # Verify results - should get exactly max_files
            assert len(results) == 2
            assert results[0].relevance_score == 0.7
            assert results[1].relevance_score == 0.6