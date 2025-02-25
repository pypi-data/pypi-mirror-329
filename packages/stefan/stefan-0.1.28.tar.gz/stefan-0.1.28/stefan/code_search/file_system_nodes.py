from pathlib import Path
from typing import List
from pydantic import BaseModel, computed_field
from datetime import datetime

class FileSystemNode(BaseModel):
    name: str
    path: Path
    last_modified: datetime

    # Dynamic calculated fields
    should_be_recalculated: bool | None = None
    public_interface: str | None = None
    description: str | None = None

    @computed_field
    @property
    def full_path(self) -> str:
        return str(self.path.absolute())

class FileNode(FileSystemNode):
    file_size: int
    file_hash: str

    @computed_field
    @property
    def extension(self) -> str:
        return self.path.suffix[1:] if self.path.suffix else None

class DirectoryNode(FileSystemNode):
    children: List['FileSystemNode'] = []

    @computed_field
    @property
    def files(self) -> List[FileNode]:
        return [node for node in self.children if isinstance(node, FileNode)]
    
    @computed_field
    @property
    def directories(self) -> List['DirectoryNode']:
        return [node for node in self.children if isinstance(node, DirectoryNode)]
    
class FileSystemTree(BaseModel):
    root: DirectoryNode

    @computed_field
    @property
    def all_files(self) -> List[FileNode]:
        return self._collect_files_recursive(self.root)
    
    def _collect_files_recursive(self, directory: DirectoryNode) -> List[FileNode]:
        files = directory.files.copy()
        for subdir in directory.directories:
            files.extend(self._collect_files_recursive(subdir))
        return files

