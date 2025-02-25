from pathlib import Path
from typing import List

from pydantic import BaseModel

from stefan.code_search.code_search_persistence import CodeSearchPersistence
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.code_search_tree_processor import CodeSearchTreeProcessor
from stefan.code_search.file_system_nodes import DirectoryNode, FileSystemNode, FileNode, FileSystemTree
from stefan.code_search.llm.llm_file_relevancy import FileRelevancyLLMProcessor, FileRelevancyResult
from stefan.execution_context import ExecutionContext
from stefan.project_configuration import ProjectContext

class CodeSearchFullTextWithRelevancyResult(BaseModel):
    file_path: Path
    relevance_score: float
    explanation: str

class CodeSearchFullTextWithRelevancy:

    def __init__(
        self,
        tree_builder: CodeSearchTreeCreator,
        llm_file_relevancy: FileRelevancyLLMProcessor,
        project_context: ProjectContext,
    ):
        self.tree_builder = tree_builder
        self.llm_file_relevancy = llm_file_relevancy
        self.project_context = project_context

    def perform_search_fulltext_with_relevancy(
        self,
        fulltext_search_query: str,
        llm_query: str,
        context: ExecutionContext,
    ) -> List[CodeSearchFullTextWithRelevancyResult]:
        # Construct the tree
        code_search_tree = self._construct_tree()

        # Traverse the tree
        found_files = self._traverse_tree_recursive(
            node=code_search_tree.root,
            fulltext_search_query=fulltext_search_query,
        )

        # Create a mapping of file paths to their nodes for reliable lookup
        file_map = {file.path: file for file in found_files}
        
        # Find the most relevant files
        relevancy_results = self.llm_file_relevancy.determine_relevancy(
            query=llm_query,
            file_nodes=found_files,
            context=context,
        )

        # Convert to results using the file map to ensure correct matching
        search_results = [
            CodeSearchFullTextWithRelevancyResult(
                file_path=file_map[relevancy_result.file_path].path,
                relevance_score=relevancy_result.relevance_score,
                explanation=relevancy_result.explanation,
            )
            for relevancy_result in relevancy_results
            if relevancy_result.is_relevant
        ]

        # Return the results
        return search_results
    
    def _traverse_tree_recursive(self, node: FileSystemNode, fulltext_search_query: str) -> List[FileNode]:
        if isinstance(node, FileNode):
            if fulltext_search_query in self._get_file_content(node.path):
                return [node]
            return []
        if isinstance(node, DirectoryNode):
            results = []
            for child in node.children:
                results.extend(self._traverse_tree_recursive(child, fulltext_search_query))
            return results
        
    def _get_file_content(self, file_path: Path) -> str:
        with open(file_path, "r") as file:
            return file.read()
        

    def _construct_tree(self) -> FileSystemTree:
        return self.tree_builder.build_file_tree(
            directory=self.project_context.root_directory,
        )
