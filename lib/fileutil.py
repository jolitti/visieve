from PIL import Image
import os
from os import path
from pathlib import Path

IMAGE_EXTENSIONS = { ex for ex,f in Image.registered_extensions().items() }

def is_valid_image_file(filepath:str) -> bool:
    _filename, fileextension = os.path.splitext(filepath)
    return fileextension in IMAGE_EXTENSIONS

def count_image_files(path:str) -> int:
    """
    Returns a count of all the files in the path folder that
    can be opened by a PIL Image
    """
    counter = 0
    for filepath in Path(os.fsdecode(path)).iterdir():
        if is_valid_image_file(filepath): counter += 1
    return counter
    

if __name__ == "__main__":
    """ exts = Image.registered_extensions()
    supported = { ex for ex,f in exts.items() }
    print(supported) """
    print(count_image_files("./example/dest1/"))

def get_unique_filename(filename:str) -> str:
    if not path.exists(filename): return filename
    else:
        prefix, suffix = os.path.splitext(filename)
        counter = 1
        while True:
            newname = f"{prefix}({counter}){suffix}"
            if not path.exists(newname): return newname
            counter += 1