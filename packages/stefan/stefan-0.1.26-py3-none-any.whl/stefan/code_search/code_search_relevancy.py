from pathlib import Path
from typing import List

from pydantic import BaseModel

from stefan.code_search.code_search_persistence import CodeSearchPersistence
from stefan.code_search.code_search_tree_creator import CodeSearchTreeCreator
from stefan.code_search.code_search_tree_processor import CodeSearchTreeProcessor
from stefan.code_search.file_system_nodes import FileSystemNode, FileNode, FileSystemTree
from stefan.code_search.llm.llm_file_relevancy import FileRelevancyLLMProcessor, FileRelevancyResult
from stefan.execution_context import ExecutionContext
from stefan.project_configuration import ProjectContext

class CodeSearchRelevancyResult(BaseModel):
    file_path: Path
    file_description: str
    file_public_interface: str
    relevance_score: float
    explanation: str

class CodeSearchRelevancy:
    def __init__(
        self,
        tree_processor: CodeSearchTreeProcessor,
        tree_builder: CodeSearchTreeCreator,
        llm_file_relevancy: FileRelevancyLLMProcessor,
        persistence: CodeSearchPersistence,
        project_context: ProjectContext,
    ):
        self.tree_processor = tree_processor
        self.tree_builder = tree_builder
        self.llm_file_relevancy = llm_file_relevancy
        self.persistence = persistence
        self.project_context = project_context

    def perform_search_with_query(
        self,
        query: str,
        max_files: int,
        select_all_high_relevant_files: bool,
        context: ExecutionContext,
    ) -> List[CodeSearchRelevancyResult]:
        # Construct the tree
        code_search_tree = self._construct_tree()

        # Get all files
        all_files = code_search_tree.all_files

        # Find the most relevant files
        relevancy_results = self.llm_file_relevancy.determine_relevancy(
            query=query,
            file_nodes=all_files,
            context=context,
        )

        # Select the relevant files (filter, sort and map to FileNode)
        relevant_files = self._select_relevant_files(all_files, relevancy_results, max_files, select_all_high_relevant_files)

        # Convert FileNodes to CodeSearchResults
        search_results = []
        relevancy_map = {result.file_path: result for result in relevancy_results}
        
        for file in relevant_files:
            relevancy_result = relevancy_map[file.path]
            result = CodeSearchRelevancyResult(
                file_path=file.path,
                file_description=file.description,
                file_public_interface=file.public_interface,
                relevance_score=relevancy_result.relevance_score,
                explanation=relevancy_result.explanation,
            )
            search_results.append(result)

        return search_results
    
    def _select_relevant_files(
        self,
        all_files: List[FileNode],
        relevancy_results: List[FileRelevancyResult],
        max_files: int,
        select_all_high_relevant_files: bool,
    ) -> List[FileNode]:
        # Create a mapping of file paths to their scores for efficient lookup
        relevancy_map = {result.file_path: result for result in relevancy_results}
        
        # Filter and sort relevant files
        relevant_files = [result.file_path for result in relevancy_results if result.is_relevant]
        relevant_files.sort(key=lambda x: relevancy_map[x].relevance_score, reverse=True)
        
        # Map file paths back to FileNode objects
        selected_relevant_files = []
        for file_path in relevant_files:
            score = relevancy_map[file_path].relevance_score
            
            # Check if we should add this file
            should_add = (
                len(selected_relevant_files) < max_files or  # Under max limit
                (select_all_high_relevant_files and score > 0.8)  # High relevance override
            )
            if not should_add:
                break
            
            # Find and add the corresponding FileNode
            for file in all_files:
                if file.path == file_path:
                    selected_relevant_files.append(file)
                    break

        return selected_relevant_files

    def _construct_tree(self) -> FileSystemTree:
        # Construct the path to the tree file relative to project root
        tree_file_path = self.project_context.execution_directory / "code_search_tree.json"

        # Load (from stored json)
        loaded_tree = self.persistence.try_load_tree(tree_file_path)

        # Create the tree (from file system)
        newly_created_tree = self.tree_builder.build_file_tree(
            directory=self.project_context.root_directory,
            include_patterns=self.project_context.include_patterns,
            exclude_patterns=self.project_context.exclude_patterns,
        )
        
        # Compare the trees and update the newly created tree with the loaded tree
        if loaded_tree is not None:
            self.tree_builder.compare_trees_and_mark_recalculation(loaded_tree, newly_created_tree)
        else:
            self.tree_builder.mark_all_for_recalculation(newly_created_tree)

        # Process the tree (calculate descriptions and public interface)
        self.tree_processor.process_tree(newly_created_tree)

        # Save the tree to the file
        self.persistence.save_tree(newly_created_tree, tree_file_path)

        # Return the processed tree
        return newly_created_tree
