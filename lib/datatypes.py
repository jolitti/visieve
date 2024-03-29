from enum import Enum
import os
from os import path
from dataclasses import dataclass

VALID_KEYS = r"1234567890abcdefghijklmnopqrtuvwxyz"

class SieveMode(Enum):
    """General operation to apply to items in the source directory"""
    COPY = "copy"
    MOVE = "move"

VALID_STATES = {SieveMode.COPY, SieveMode.MOVE}

class DuplicateMode(Enum):
    """Policy to apply to duplicate filenames"""
    MAINTAIN = "maintain"
    """The already existing file takes precendence"""
    OVERWRITE = "overwrite"
    """The new file takes precedence"""
    ASSIGN_UNIQUE_NAME = "assign new name"
    """Attempt to add a numeric suffix that distinguishes the new file"""
    HALT = "halt"
    """Send an error message to the user and crash the program"""


@dataclass
class InstanceConfig:
    """Configuration data needed for sorting"""
    source:str
    dest: dict[str,str]
    sieve_mode: SieveMode = SieveMode.COPY
    duplicate_mode: DuplicateMode = DuplicateMode.ASSIGN_UNIQUE_NAME
    size:tuple[int,int] = (600,600)

    def is_valid(self) -> bool | str:
        """Verify whether this configuration actually represents a working setting"""
        if self.sieve_mode not in VALID_STATES: return "Invalid state"
        if self.source is None: return "Source dir is None"
        if not path.exists(self.source): return "Non existent source dir"
        if self.dest is None: return "Destination dictionary is None"
        for _,dest in self.dest.items():
            if not path.exists(dest): return "Non existent destination dir"
        return True

    def get_size_string(self) -> str:
        """Format the self.size tuple into a '100x100'-type string"""
        width, height = self.size
        return f"{width}x{height}"

    def are_destinations_empty(self) -> bool:
        """Returns True if all of the destinations directories are empty"""
        for _,dirpath in self.dest.items():
            if os.listdir(dirpath): return False
        return True

    def is_source_empty(self) -> bool:
        """Returns True if the source directory is empty"""
        return not os.listdir(self.source)


if __name__ == "__main__":
    print(SieveMode["halt"])