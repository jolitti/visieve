from lib.bind_util import open_bind_dialog
from lib.sorter import open_sorting_window
import sys

result = open_bind_dialog()

if not result:
    print("Quitting...")
    sys.exit()

print("Beginning the sieving process")

open_sorting_window(result)
