import random
from .datatypes import InstanceConfig

source = "example/airfreight/"
destinations = {
        "a": "example/dest1/", 
        "s": "example/dest2/"
        }
sample_answer = (source,destinations)

def open_bind_dialog() -> InstanceConfig:
    return random.choice([sample_answer, None])
