import tkinter as tk

from .datatypes import InstanceConfig
from .datatypes import SieveMode, DuplicateMode
from .custom_widgets import CompleteKeyDirBinder, FolderPicker

sievemode_list = [ x.value for x in SieveMode ]
sievemode_dict = { x.value:x for x in SieveMode }
dupmode_list = [ x.value for x in DuplicateMode ]
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

        # source directory selector
        self.source_selector = FolderPicker(self.window,text="Select source folder")
        self.source_selector.pack()

        # KeyDirPair().pack()
        self.kdbind = CompleteKeyDirBinder()
        self.kdbind.pack()

        tk.Button(text="Print settings",command=self._print_kdbind).pack()

        self.window.protocol("WM_DELETE_WINDOW",self.set_instance_config)

        self.window.mainloop()

    def set_instance_config(self) -> InstanceConfig:
        """
        To be called while the window is closing.
        Will collect information from the various widgets and save them
        in an IntanceConfig object, appending it into self.answer_holder
        """
        sievemode = sievemode_dict[self.sievemode_text.get()]
        dupmode = dupmode_dict[self.dupmode_text.get()]
        source = self.source_selector.get_folder_path()
        bindings = self.kdbind.get_binding_pairs()

        self.answer_holder.append(InstanceConfig(
            source,
            bindings,
            sievemode,
            dupmode
        ))

        self.window.destroy()

    def _print_kdbind(self):
        print(self.kdbind.get_binding_pairs())


def open_bind_dialog() -> InstanceConfig:
    answer_list = []
    dialog = BindingDialog(answer_list)

    if len(answer_list) <= 0: raise ValueError("Dialog didn't put anything in answer_list")
    answer = answer_list[-1]
    if not isinstance(answer,InstanceConfig): raise ValueError("Dialog didn't produce a config")
    if not answer.is_valid(): raise ValueError("Dialog didn't produce a valid config")

    return answer
