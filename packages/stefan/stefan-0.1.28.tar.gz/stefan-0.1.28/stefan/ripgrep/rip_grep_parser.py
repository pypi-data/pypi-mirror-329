import json

from typing import List
from pydantic import BaseModel

class RipGrepLine(BaseModel):
    text: str
    line_number: int

class RipGrepFile(BaseModel):
    file_path: str
    lines: List[RipGrepLine]

    @property
    def stringified(self) -> str:
        result = f"File: {self.file_path}\n"
        last_line_number = None
        for line in self.lines:
            if last_line_number is not None and line.line_number > last_line_number + 1:
                result += "----------------------------------------\n"
            result += f"{line.line_number}: {line.text}\n"
            last_line_number = line.line_number

        return result
    
class RipGrepResult(BaseModel):
    files: List[RipGrepFile]

    @property
    def stringified(self) -> str:
        if len(self.files) == 0:
            return "No results found"
        
        summary = f"Found {len(self.files)} files\n\n"
        files = "\n\n".join([file.stringified for file in self.files])

        return summary + files

class RipGrepParser:
    def parse_ripgrep_output(self, json_lines: str, directory: str) -> RipGrepResult:
        files: dict[str, RipGrepFile] = {}
        current_file = None
        
        # Handle empty input case
        if not json_lines:
            return RipGrepResult(files=[])
        
        for line in json_lines.splitlines():
            if not line:
                continue
            
            try:
                data = json.loads(line)
                
                if data["type"] == "begin":
                    file_path = data["data"]["path"]["text"]
                    current_file = file_path
                    if file_path not in files:
                        if len(directory) == 0 or directory == ".":
                            full_file_path = file_path
                        elif directory.endswith("/"):
                            full_file_path = directory + file_path
                        else:
                            full_file_path = directory + "/" + file_path
                        files[file_path] = RipGrepFile(file_path=full_file_path, lines=[])
                        
                elif data["type"] in ["match", "context"]:
                    if current_file:
                        files[current_file].lines.append(
                            RipGrepLine(
                                text=data["data"]["lines"]["text"].rstrip(),
                                line_number=data["data"]["line_number"]
                            )
                        )
            except json.JSONDecodeError:
                raise Exception("Invalid JSON input")

        return RipGrepResult(files=list(files.values()))