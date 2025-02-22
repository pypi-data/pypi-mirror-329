from pathlib import Path
from typing import List

from pydantic import BaseModel

from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.file_system_nodes import (
    DirectoryNode,
    FileNode,
    FileSystemNode,
    FileSystemTree,
)
from stefan.execution_context import ExecutionContext
from stefan.project_configuration import ProjectContext


class CodeSearchFullTextResult(BaseModel):
    file_path: Path

class CodeSearchFullText:

    def __init__(
        self,
        tree_builder: CodeSearchTreeCreator,
        project_context: ProjectContext,
    ):
        self.tree_builder = tree_builder
        self.project_context = project_context

    def perform_search_fulltext(
        self,
        fulltext_search_query: str,
        context: ExecutionContext,
    ) -> List[CodeSearchFullTextResult]:
        # Construct the tree
        code_search_tree = self._construct_tree()

        # Traverse the tree
        found_files = self._traverse_tree_recursive(
            node=code_search_tree.root,
            fulltext_search_query=fulltext_search_query,
        )
        
        # Convert FileNodes to CodeSearchResults
        search_results = [CodeSearchFullTextResult(file_path=file.path) for file in found_files]

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
