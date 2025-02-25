from pathlib import Path
from typing import Optional, List
from stefan.code_search.file_system_nodes import FileSystemNode, DirectoryNode, FileNode, FileSystemTree
from stefan.code_search.llm.llm_directory_description import DirectoryDescriptionLLMProcessor
from stefan.code_search.llm.llm_file_description import FileDescriptionLLMProcessor
from stefan.utils.async_execution import AsyncExecution

class CodeSearchTreeProcessor:
    def __init__(
        self,
        llm_file_processor: FileDescriptionLLMProcessor,
        llm_directory_processor: DirectoryDescriptionLLMProcessor,
    ):
        self.llm_file_processor = llm_file_processor
        self.llm_directory_processor = llm_directory_processor

    def process_tree(self, tree: FileSystemTree, process_directories: bool = False) -> None:
        # Collect all file nodes that need processing
        file_nodes = self._collect_file_nodes(tree.root)
        
        # Process files in parallel
        if file_nodes:
            args_list = [(node,) for node in file_nodes]
            AsyncExecution.run_async_tasks_in_executor(
                self._process_file,
                *args_list
            )

        if process_directories:
            while True:
                directory_nodes = self._collect_directory_nodes_ready_for_processing(tree.root)
                if not directory_nodes:
                    break
                args_list = [(node,) for node in directory_nodes]
                AsyncExecution.run_async_tasks_in_executor(
                    self._process_directory,
                    *args_list
                )

    def _collect_file_nodes(self, node: FileSystemNode) -> List[FileNode]:
        """
        Recursively collect all file nodes that need to be processed.
        """
        if node.should_be_recalculated is None:
            raise ValueError(f"Node {node.name} has should_be_recalculated set to None")

        if isinstance(node, FileNode):
            return [node] if node.should_be_recalculated else []
        elif isinstance(node, DirectoryNode):
            return [
                file_node
                for child in node.children
                for file_node in self._collect_file_nodes(child)
            ]
        return []
    
    def _collect_directory_nodes_ready_for_processing(self, node: FileSystemNode) -> List[DirectoryNode]:
        """
        Recursively collect all "leaf" directory nodes that need to be processed.
        A directory is ready for processing if:
        1. It needs recalculation (should_be_recalculated is True)
        2. All its children have descriptions
        3. None of its subdirectories need processing
        """
        # Invalid state check
        if node.should_be_recalculated is None:
            raise ValueError(f"Node {node.name} has should_be_recalculated set to None")
        
        # If node is not a directory node, return empty list
        if isinstance(node, FileNode):
            return []
        
        if not isinstance(node, DirectoryNode):
            raise ValueError(f"Node {node.name} is not a directory node. Node: {node}")

        # First, check children for ready directories
        ready_child_dirs = [
            dir_node
            for child in node.children
            for dir_node in self._collect_directory_nodes_ready_for_processing(child)
        ]
        
        # If any child directories are ready, return those
        if ready_child_dirs:
            return ready_child_dirs
        
        # If no child directories are ready and this directory needs processing
        # and all its children have descriptions, then this is a leaf ready for processing
        if node.should_be_recalculated and all(child.description is not None for child in node.children):
            return [node]
        
        return []

    def _process_file(self, node: FileNode) -> None:
        """
        Process a file node by reading its content and generating a description.
        """
        with open(node.path, 'r', encoding='utf-8') as f:
            content = f.read()
        result = self.llm_file_processor.extract_public_interface_and_description(
            file_content=content,
            file_path=str(node.path)
        )
        node.public_interface = result.public_interface
        node.description = result.description

    def _process_directory(self, node: DirectoryNode) -> None:
        """
        Process a directory node by generating a description.
        """
        result = self.llm_directory_processor.extract_directory_description(
            directory_node=node,
        )
        node.description = result.description
