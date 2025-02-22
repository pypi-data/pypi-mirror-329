import os

class FileWriter:

    @staticmethod
    def write_file(file_path: str, content: str, mode: str = 'w') -> str:
        """
        Writes content to a file.
        
        Args:
            file_path (str): Path to the file to write to
            content (str): Content to write to the file
            mode (str): Write mode ('w' for overwrite, 'a' for append)
            
        Returns:
            str: Success or error message
        """
        try:
            # Input validation
            if mode not in ['w', 'a']:
                return f"Error: Invalid mode '{mode}'. Must be 'w' (write) or 'a' (append)"
            
            # Normalize path
            file_path = os.path.abspath(os.path.normpath(file_path))
            
            # Check if directory exists
            directory = os.path.dirname(file_path)
            if not os.path.exists(directory):
                os.makedirs(directory, exist_ok=True)
            
            # Write to the file
            with open(file_path, mode, encoding='utf-8') as file:
                file.write(content)
            
            return f"Successfully wrote to file: {file_path}"
        except Exception as e:
            return f"Error writing to file {file_path}: {str(e)}"
    
    @staticmethod
    def write_multiple_files(file_content_map: dict[str, str], mode: str = 'w') -> list[str]:
        """
        Writes content to multiple files.
        
        Args:
            file_content_map (dict[str, str]): Dictionary mapping file paths to their contents
            mode (str): Write mode ('w' for overwrite, 'a' for append)
            
        Returns:
            list[str]: List of success/error messages for each file
        """
        results = []
        
        for file_path, content in file_content_map.items():
            result = FileWriter.write_file(file_path, content, mode)
            results.append(result)
        
        return results
