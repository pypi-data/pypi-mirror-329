from typing import List

class FileReader:

    @staticmethod
    def read_single_file(file_path: str) -> str:
        """Read a single file and return its content with proper formatting."""
        with open(file_path, 'r') as file:
            content = file.read()
            return f'<file_content>\n{content}\n</file_content>'
    
    @staticmethod
    def read_multiple_files(file_paths: List[str]) -> str:
        """Read multiple files and return their contents with proper formatting."""
        result = []
        for file_path in file_paths:
            try:
                content = FileReader.read_single_file(file_path)
                result.append(f'File: {file_path}\n{content}\n')
            except Exception as e:
                result.append(f'Error reading {file_path}: {str(e)}\n')
        return ''.join(result)