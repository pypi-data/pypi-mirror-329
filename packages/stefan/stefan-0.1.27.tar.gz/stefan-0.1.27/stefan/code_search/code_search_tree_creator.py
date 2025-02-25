from pathlib import Path
from typing import List, Dict
import hashlib
import fnmatch
from datetime import datetime

from stefan.code_search.file_system_nodes import FileSystemNode, DirectoryNode, FileNode, FileSystemTree
from stefan.project_configuration import ProjectContext

class CodeSearchTreeCreator:

    def __init__(
        self,
        project_context: ProjectContext,
    ):
        self.project_context = project_context

    def build_file_tree(
        self,
        directory: Path,
        include_patterns: List[str] | None = None,
        exclude_patterns: List[str] | None = None,
    ) -> FileSystemTree:
        include_patterns = include_patterns or self.project_context.include_patterns
        exclude_patterns = exclude_patterns or self.project_context.exclude_patterns
        root = self._build_file_tree_recursive(directory, include_patterns, exclude_patterns)
        return FileSystemTree(root=root)

    def _build_file_tree_recursive(
        self,
        directory: Path,
        include_patterns: List[str],
        exclude_patterns: List[str],
    ) -> FileSystemNode:
        """
        Build a tree structure of files and directories.
        
        Args:
            directory: Root directory to start scanning
        """
        path = Path(directory)
        name = path.name or str(path)
        is_dir = path.is_dir()

        # Check if path should be excluded
        for pattern in exclude_patterns:
            if fnmatch.fnmatch(name, pattern):
                return None

        if is_dir:
            children = []
            for item in path.iterdir():
                child_node = self._build_file_tree_recursive(item, include_patterns, exclude_patterns)
                if child_node:
                    children.append(child_node)
            
            return DirectoryNode(
                path=path,
                name=name,
                last_modified=datetime.fromtimestamp(path.stat().st_mtime),
                children=children,
            )
        else:
            # Check if file matches include patterns
            included = any(fnmatch.fnmatch(name, pattern) for pattern in include_patterns)
            if not included:
                return None
                
            stat = path.stat()
            return FileNode(
                path=path,
                name=name,
                last_modified=datetime.fromtimestamp(stat.st_mtime),
                file_size=stat.st_size,
                file_hash=self._calculate_file_hash(path)
            )

    def compare_trees_and_mark_recalculation(
        self,
        old_tree: FileSystemTree,
        new_tree: FileSystemTree,
    ):
        """
        Compare two file trees and set should_be_recalculated flag on new_tree nodes based on changes.
        """
        def get_file_dict(root: FileSystemNode) -> Dict[str, FileNode]:
            result = {}
            if isinstance(root, DirectoryNode) and root.children:
                for child in root.children:
                    if isinstance(child, DirectoryNode):
                        result.update(get_file_dict(child))
                    elif isinstance(child, FileNode):
                        result[str(child.path)] = child
            return result
        
        def get_dir_dict(node: FileSystemNode) -> Dict[str, DirectoryNode]:
            result = {}
            if isinstance(node, DirectoryNode):
                result[str(node.path)] = node
                for child in node.children:
                    if isinstance(child, DirectoryNode):
                        result.update(get_dir_dict(child))
            return result

        def mark_recalculation_flags(new_node: FileSystemNode, old_files: Dict[str, FileNode], old_dirs: Dict[str, DirectoryNode]) -> bool:
            """
            Recursively mark should_be_recalculated flags and return if any child needs recalculation
            """
            path_str = str(new_node.path)
            
            if isinstance(new_node, FileNode):
                if path_str in old_files:
                    # Existing file - check if modified
                    old_file = old_files[path_str]
                    new_node.should_be_recalculated = new_node.file_hash != old_file.file_hash
                    # Copy description if no recalculation needed
                    if not new_node.should_be_recalculated:
                        new_node.public_interface = old_file.public_interface
                        new_node.description = old_file.description
                else:
                    # New file
                    new_node.should_be_recalculated = True
                return new_node.should_be_recalculated
            
            elif isinstance(new_node, DirectoryNode):
                # Check if directory existed before
                dir_existed = path_str in old_dirs
                old_dir = old_dirs.get(path_str)
                
                # Process all children first
                needs_recalc = False
                for child in new_node.children:
                    if mark_recalculation_flags(child, old_files, old_dirs):
                        needs_recalc = True
                
                # Directory needs recalculation if:
                # 1. Any child needs recalculation
                # 2. Directory is new
                # 3. Directory had different children before
                if old_dir:
                    old_children_paths = {str(c.path) for c in old_dir.children}
                    new_children_paths = {str(c.path) for c in new_node.children}
                    if old_children_paths != new_children_paths:
                        needs_recalc = True
                
                new_node.should_be_recalculated = needs_recalc or not dir_existed
                # Copy description if no recalculation needed
                if not new_node.should_be_recalculated and old_dir:
                    new_node.description = old_dir.description
                return new_node.should_be_recalculated
            
            return False

        old_files = get_file_dict(old_tree.root)
        old_dirs = get_dir_dict(old_tree.root)
        
        # Mark recalculation flags on the entire new tree
        mark_recalculation_flags(new_tree.root, old_files, old_dirs)

    def mark_all_for_recalculation(self, tree: FileSystemTree):
        """Mark all nodes for recalculation"""
        def mark_recursive(node: FileSystemNode):
            node.should_be_recalculated = True
            if isinstance(node, DirectoryNode) and node.children:
                for child in node.children:
                    mark_recursive(child)
    
        mark_recursive(tree.root)

    def _calculate_file_hash(
        self,
        file_path: Path
    ) -> str:
        """Calculate SHA-256 hash of a file."""
        sha256_hash = hashlib.sha256()
        
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        
        return sha256_hash.hexdigest()