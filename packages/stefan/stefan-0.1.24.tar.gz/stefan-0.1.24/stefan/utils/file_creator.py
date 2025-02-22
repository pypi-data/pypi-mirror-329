import os

class FileCreator:

    @classmethod
    def create_file(cls, file_path: str, content: str) -> str:
        """
        Creates a file with the specified content.
        
        Args:
            file_path (str): Path where the file should be created
            content (str): Content to write to the file
            
        Returns:
            tuple[bool, str]: (success status, message)
        """
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            
            with open(file_path, "w") as file:
                file.write(content)
            
            return f"Successfully created file: {file_path}"
        except Exception as e:
            return f"Error creating file {file_path}: {str(e)}"
        
    @classmethod
    def create_multiple_files(cls, files_dict: dict[str, str]) -> list[str]:
        """
        Creates multiple files with their specified contents.
        
        Args:
            files_dict (dict[str, str]): Dictionary mapping file paths to their contents
            
        Returns:
            list[tuple[bool, str]]: List of (success status, message) for each file
        """
        results = []
        
        for file_path, content in files_dict.items():
            result = cls.create_file(file_path, content)
            results.append(result)
        
        return results
    
    
