from enum import Enum
from os import path
from dataclasses import dataclass

VALID_KEYS = r"1234567890abcdefghijklmnopqrtuvwxyz"

class SieveMode(Enum):
    """General operation to apply to items in the source directory"""
    COPY = "copy"
    MOVE = "move"
    INVALID = "invalid"

VALID_STATES = {SieveMode.COPY, SieveMode.MOVE}

@dataclass(frozen=True)
class InstanceConfig:
    """Configuration data needed for sorting"""
    source:str
    dest: dict[str,str]
    mode: SieveMode = SieveMode.COPY
    size:tuple[int,int] = (600,600)

    def is_valid(self) -> bool:
        """Verify whether this configuration actually represents a working setting"""
        if self.mode not in VALID_STATES: return False
        if not path.exists(self.source): return False
        for _,dest in self.dest.items():
            if not path.exists(dest): return False
        return True
