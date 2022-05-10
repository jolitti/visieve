import tkinter as tk

from .datatypes import InstanceConfig
from .datatypes import SieveMode, DuplicateMode
from .custom_widgets import KeyDirList, KeyDirPair

sievemode_list = [x.value for x in SieveMode]
sievemode_dict = { x.value:x for x in SieveMode }
dupmode_list = [x.value for x in DuplicateMode]
dupmode_dict = { x.value:x for x in DuplicateMode }

# artefact from when the configuration was just a tuple
# of a source str and a destination dict
""" source = "example/airfreight/"
destinations = {
        "a": "example/dest1/", 
        "s": "example/dest2/"
        }
sample_answer = (source,destinations) """

class BindingDialog:
    """
    Object that represents a tkinter window where the user can configure the settings for a sorter.SortingDialog
    Initialization requires an external list to store the produced InstanceConfig
    """

    def __init__(self, answer_holder: list) -> None:
        self.window = tk.Tk()
        self.answer_holder = answer_holder
        if not isinstance(self.answer_holder,list): raise ValueError("answer_holder is not a list!")

        # selector for the sievemode
        self.sievemode_text = tk.StringVar(self.window,sievemode_list[0])
        self.sievemode_selector = tk.OptionMenu(self.window,self.sievemode_text,*sievemode_list)
        self.sievemode_selector.pack()

        # selector for the duplicatemode
        self.dupmode_text = tk.StringVar(self.window,dupmode_list[0])
        self.dupmode_selector = tk.OptionMenu(self.window,self.dupmode_text,*dupmode_list)
        self.dupmode_selector.pack()

        # KeyDirPair().pack()
        kdlist = KeyDirList()
        kdlist.add_pair()
        kdlist.add_pair()
        kdlist.pack()

        tk.Button(text="Add pair",command=kdlist.add_pair).pack()
        tk.Button(text="Remove pair",command=kdlist.remove_pair).pack()

        self.window.mainloop()

    def set_instance_config(self) -> InstanceConfig:
        """
        To be called while the window is closing.
        Will collect information from the various widgets and save them
        in an IntanceConfig object, appending it into self.answer_holder
        """
        pass


def open_bind_dialog() -> InstanceConfig:
    answer_list = []
    dialog = BindingDialog(answer_list)

    if len(answer_list) <= 0: raise ValueError("Dialog didn't put anything in answer_list")
    answer = answer_list[-1]
    if not isinstance(answer,InstanceConfig): raise ValueError("Dialog didn't produce a config")
    if not answer.is_valid(): raise ValueError("Dialog didn't produce a valid config")

    return answer
