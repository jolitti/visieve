from lib.bind_util import open_bind_dialog
from lib.sorter import open_sorting_window
from lib.datatypes import InstanceConfig, SieveMode
import sys

result = open_bind_dialog()

result = InstanceConfig(
    mode=SieveMode.COPY,
    source="example/afreightdata/",
    dest={
        "a": "example/dest1/",
        "b": "example/dest2/",
        "c": "example/dest3/"
    }
    )

print(result)

if not result:
    print("Quitting...")
    sys.exit()

print("Beginning the sieving process")

open_sorting_window(result)

print("Done. Thanks for using visieve!")