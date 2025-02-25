from typing import List
from stefan.project_configuration import ProjectContext
from stefan.ripgrep.rip_grep_parser import RipGrepParser, RipGrepResult
import subprocess
import shlex

class RipGrepSearch:
    def __init__(self, context: ProjectContext):
        self.context = context

    def search(self, command: str, directory: str) -> RipGrepResult:
        # Check if --json flag is present, if not add it
        if '--json' not in command:
            command = f"{command} --json"

        # Split the command into arguments while preserving quoted strings
        args = shlex.split(command)
        
        try:
            # Execute the ripgrep command
            process = subprocess.run(
                args,
                cwd=directory,
                capture_output=True,
                text=True
            )
            
            # Check stderr first
            if process.stderr:
                raise RuntimeError(f"Ripgrep error: {process.stderr}")
            
            # Get the stdout output
            output = process.stdout
            
            # If there's no output, return empty result
            if not output:
                return []
            
            # Process the output through ripgrep parser
            return RipGrepParser().parse_ripgrep_output(
                json_lines=output,
                directory=directory,
            )
        except subprocess.SubprocessError as e:
            # Handle any subprocess errors
            raise RuntimeError(f"Failed to execute ripgrep search: {str(e)}")
