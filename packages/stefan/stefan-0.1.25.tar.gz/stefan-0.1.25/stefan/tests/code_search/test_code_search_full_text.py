import pytest
from pathlib import Path
import tempfile

from stefan.code_search.code_search_full_text import CodeSearchFullText
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.execution_context import ExecutionContext
from stefan.tests.fixtures.dummy_project_context import create_dummy_project_context

class TestCodeSearchFullText:
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
            
            # Create Python files with specific content for full-text search
            (root / "file1.py").write_text("def search_function(): return 'searchable content'")
            (root / "dir1" / "file2.py").write_text("class SearchClass:\n    search_term = 'findable'")
            (root / "dir1" / "subdir" / "file3.py").write_text("# This file has no search terms")
            (root / "dir2" / "file4.txt").write_text("searchable but not a python file")
            
            yield root

    @pytest.fixture
    def code_search(self, temp_directory):
        """Create CodeSearchFullText instance"""
        project_context = create_dummy_project_context(
            path=temp_directory,
            include_patterns=["*.py"],
            exclude_patterns=[".git", "__pycache__"]
        )

        tree_builder = CodeSearchTreeCreator(
            project_context=project_context,
        )
        
        return CodeSearchFullText(
            tree_builder=tree_builder,
            project_context=project_context,
        )

    def test_perform_search_finds_matching_files(
        self,
        code_search: CodeSearchFullText,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test that search finds files containing the search text"""
        # Perform search for 'searchable'
        results = code_search.perform_search_fulltext(
            fulltext_search_query="searchable",
            context=execution_context
        )
        
        # Should find only file1.py (file4.txt is excluded by file pattern)
        assert len(results) == 1
        assert results[0].file_path == temp_directory / "file1.py"

    def test_perform_search_with_multiple_matches(
        self,
        code_search: CodeSearchFullText,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test search when multiple files contain the search term"""
        # Write content with common term to multiple files
        (temp_directory / "file1.py").write_text("common_term = 'found'")
        (temp_directory / "dir1" / "file2.py").write_text("also_common_term = 'found'")
        
        results = code_search.perform_search_fulltext(
            fulltext_search_query="found",
            context=execution_context
        )
        
        assert len(results) == 2
        file_paths = {result.file_path for result in results}
        assert temp_directory / "file1.py" in file_paths
        assert temp_directory / "dir1" / "file2.py" in file_paths

    def test_perform_search_with_no_matches(
        self,
        code_search: CodeSearchFullText,
        execution_context: ExecutionContext
    ):
        """Test search when no files contain the search term"""
        results = code_search.perform_search_fulltext(
            fulltext_search_query="nonexistent_term",
            context=execution_context
        )
        
        assert len(results) == 0

    def test_perform_search_respects_file_patterns(
        self,
        code_search: CodeSearchFullText,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test that search only includes files matching the include patterns"""
        # Create both Python and text files with same content
        (temp_directory / "test.py").write_text("XXYYXX content")
        (temp_directory / "test.txt").write_text("XXYYXX content")
        
        results = code_search.perform_search_fulltext(
            fulltext_search_query="XXYYXX",
            context=execution_context
        )
        
        # Should only find the Python file
        assert len(results) == 1
        assert results[0].file_path == temp_directory / "test.py"

    def test_perform_search_case_sensitive(
        self,
        code_search: CodeSearchFullText,
        temp_directory: Path,
        execution_context: ExecutionContext
    ):
        """Test that search is case-sensitive"""
        (temp_directory / "file1.py").write_text("UPPERCASE = 'TEST'")
        
        # Search for lowercase
        results_lower = code_search.perform_search_fulltext(
            fulltext_search_query="test",
            context=execution_context
        )
        
        # Search for uppercase
        results_upper = code_search.perform_search_fulltext(
            fulltext_search_query="TEST",
            context=execution_context
        )
        
        assert len(results_lower) == 0
        assert len(results_upper) == 1 