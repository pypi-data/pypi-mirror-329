import subprocess
from typing import Tuple

class CommandExecutor:
    @staticmethod
    def execute(command: str) -> Tuple[bool, str]:
        """
        Execute a command line command and return the results
        
        Args:
            command: Command to execute as a string
            
        Returns:
            Tuple[bool, str]: A tuple containing:
                - bool: True if command executed successfully, False if failed
                - str: Combined output message from stdout and stderr
        """
        try:
            # Run the command as a shell command to preserve spacing
            result = subprocess.run(
                command,  # Pass command as string instead of splitting
                shell=True,  # Add shell=True to preserve command structure
                capture_output=True,
                text=True,
            )
            
            # Combine stdout and stderr, preserving order if both present
            output_parts = []
            if result.stdout:
                output_parts.append(result.stdout)
            if result.stderr:
                output_parts.append(result.stderr)
            
            output = "".join(output_parts)
            
            # Check if command was successful (return code 0 means success)
            success = result.returncode == 0
            
            # Return success and output
            return success, output
                
        except Exception as e:
            return False, f"Error executing command '{command}': {str(e)}"
