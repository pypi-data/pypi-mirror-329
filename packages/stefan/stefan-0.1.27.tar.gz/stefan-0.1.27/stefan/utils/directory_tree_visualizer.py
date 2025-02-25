import os
from typing import Optional, List
import fnmatch
from stefan.project_configuration import ProjectContext

class DirectoryTreeVisualizer:
    @classmethod
    def show_directory(cls, directory: str, project_context: ProjectContext, postfix: Optional[str] = None) -> str:
        """
        Lists all files with given postfix in directory as a table of contents.
        
        Args:
            directory (str): Path to the directory to list
            postfix (Optional[str]): File extension filter (e.g., '.py')
            
        Returns:
            str: Formatted table of contents
        """

        # Start with empty patterns instead of copying from project context
        # This allows more control over when to use project patterns
        include_patterns = []
        
        # Only use patterns in two cases:
        # 1. When postfix is provided - use only that pattern
        # 2. When directory is not empty - use project context patterns
        # This ensures empty directories get the correct "No files found" message
        if postfix:
            formatted_postfix = f"*{postfix}"
            include_patterns.append(formatted_postfix)
        elif os.path.exists(directory) and any(os.scandir(directory)):
            include_patterns.extend(project_context.include_patterns)

        exclude_patterns = project_context.exclude_patterns
        return cls.show_directory_contents(directory, include_patterns, exclude_patterns)

    @classmethod
    def show_directory_contents(cls, directory: str, include_patterns: List[str], exclude_patterns: List[str]) -> str:
        if not os.path.exists(directory):
            return f"Error: Directory '{directory}' does not exist"
        
        file_list = []
        for root, dirs, files in os.walk(directory, topdown=True):
            # Check if the current directory should be excluded
            rel_path = os.path.relpath(root, directory)
            
            # Don't exclude the root directory itself, even if it matches exclude patterns
            # This fixes the issue where '.' would match '.*' pattern and exclude everything
            if rel_path != '.':
                should_exclude_dir = any(
                    fnmatch.fnmatch(rel_path, pattern) or 
                    fnmatch.fnmatch(os.path.join(rel_path, ''), pattern) or
                    fnmatch.fnmatch(os.path.basename(rel_path), pattern)
                    for pattern in exclude_patterns
                )
                
                if should_exclude_dir:
                    print(f"DEBUG: Excluding directory: {rel_path}")
                    dirs[:] = []
                    continue
            
            # Filter directories
            dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in exclude_patterns)]
            
            # Add files
            for file in sorted(files):
                should_include = not include_patterns or any(fnmatch.fnmatch(file, pattern) for pattern in include_patterns)
                should_exclude = any(fnmatch.fnmatch(file, pattern) for pattern in exclude_patterns)
                
                if should_include and not should_exclude:
                    file_path = os.path.join(rel_path, file)
                    if rel_path == '.':
                        file_path = file
                    file_list.append(f"- {file_path}")
        
        if not file_list:
            # Return different messages based on whether we're using patterns
            # This ensures empty directories get the correct message format
            if not include_patterns:
                return "No files found in directory"
            pattern_str = ', '.join(include_patterns) if include_patterns else ""
            return f"No files matching patterns: {pattern_str} found in directory"
        
        return "# Table of Contents\n" + "\n".join(file_list)
