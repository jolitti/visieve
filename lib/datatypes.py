from enum import Enum
from os import path

VALID_KEYS = r"1234567890abcdefghijklmnopqrtuvwxyz"

class SieveMode(Enum):
    COPY = "copy"
    MOVE = "move"
    INVALID = "invalid"

VALID_STATES = {SieveMode.COPY, SieveMode.MOVE}

class InstanceConfig:
    mode: SieveMode
    source:str
    destinations: dict[str,str]
    
    def __init__(self,mode:SieveMode,source:str,dest:dict[str,str]):
        self.mode = mode
        self.source = source
        self.destinations = dest

    def is_valid(self) -> bool:
        if self.mode not in VALID_STATES: return False
        if not path.exists(self.source): return False
        for _,dest in self.destinations.items():
            if not path.exists(dest): return False
        return True
