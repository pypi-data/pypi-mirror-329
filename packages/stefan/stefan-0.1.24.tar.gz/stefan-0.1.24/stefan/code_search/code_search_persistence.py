from pathlib import Path
import json
from typing import Dict, Any
from datetime import datetime

from stefan.code_search.file_system_nodes import FileSystemNode, DirectoryNode, FileNode, FileSystemTree

class CodeSearchPersistence:

    @staticmethod
    def save_tree(tree: FileSystemTree, output_file: Path) -> None:
        """
        Save the file tree structure to a JSON file.
        
        Args:
            tree: Root node of the file tree
            output_file: Path where to save the JSON file
        """
        def node_to_dict(node: FileSystemNode) -> Dict[str, Any]:
            # Convert node to dict, excluding should_be_recalculated
            node_dict = node.model_dump(
                exclude={'should_be_recalculated'},
                mode='json'  # This ensures Path objects and datetime are converted to strings
            )
            
            # Add type information
            node_dict['_type'] = node.__class__.__name__
            
            # Handle children for DirectoryNode
            if isinstance(node, DirectoryNode):
                node_dict['children'] = [node_to_dict(child) for child in node.children]
            
            return node_dict
        
        tree_dict = node_to_dict(node=tree.root)
        # Create parent directories if they don't exist
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(tree_dict, f, indent=2)

    @staticmethod
    def try_load_tree(input_file: Path) -> FileSystemTree | None:
        """
        Load the file tree structure from a JSON file.
        
        Args:
            input_file: Path to the JSON file containing the tree structure
            
        Returns:
            Reconstructed file tree with FileSystemNode as root
        """
        def dict_to_node(node_dict: Dict[str, Any]) -> FileSystemNode:
            # Remove type information
            node_type = node_dict.pop('_type')
            
            # Convert string path back to Path
            node_dict['path'] = Path(node_dict['path'])
            
            # Convert ISO format string back to datetime
            node_dict['last_modified'] = datetime.fromisoformat(node_dict['last_modified'])
            
            if node_type == 'DirectoryNode':
                # Convert children recursively
                children = node_dict.pop('children')
                node_dict['children'] = [dict_to_node(child) for child in children]
                return DirectoryNode(**node_dict)
            elif node_type == 'FileNode':
                return FileNode(**node_dict)
            else:
                raise ValueError(f"Unknown node type: {node_type}")
            
        if not input_file.exists():
            return None

        with open(input_file) as f:
            tree_dict = json.load(f)
        
        return FileSystemTree(root=dict_to_node(tree_dict))
