from doctest import master
import tkinter as tk
from tkinter import filedialog
from os import path

# ACCEPTED_KEYS = set(r"0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")

class KeyBinder(tk.Button):
    """Button that binds to a simple key (1-9 and a-z) pressed after clicking on it"""
    ACCEPTED_KEYS = set(r"0123456789abcdefghijklmnopqrstuvwxyz")
    """List of normal keys, KeyBinder will restrict only to these"""

    keycode: str
    bind_list: set[str]
    def __init__(self,bind_list:set[str]=None,*args,**kwargs):
        super().__init__(command=self.start_keybind,*args,**kwargs)
        #self.config(command=self.folder_select())
        self.keycode = None
        self.bind_list = bind_list
        if "text" not in kwargs: self.config(text="Choose key")

    def start_keybind(self):
        """Alert the application to start listening to keypresses"""
        if self.keycode: self.winfo_toplevel().unbind(self.keycode)
        self.winfo_toplevel().bind("<Key>",self.bind_key)
        self.config(text="Press a key...")

    def bind_key(self,event:tk.Event):
        """Triggered after keypress, captures its code"""
        # If event is not a char or a valid char
        if not event.char or event.char not in KeyBinder.ACCEPTED_KEYS:
            self.keycode = None
            self.config(text="Choose key")
        # If we don't have a bind list or the new char is not in the list
        elif not self.bind_list or event.keycode not in self.bind_list:
            self.keycode = event.keysym.lower()
            self.config(text=event.keysym)
            # if we do have a bind_list, add the new char to it
            if self.bind_list: self.bind_list.add(self.keycode)
        else:
            self.keycode = None
            self.config(text="Key already bound")
        # in any case, stop listening for keypresses
        self.winfo_toplevel().unbind("<Key>")
        #print(self.key_code)

    def get_keycode(self) -> str | None:
        """Returns the bound keycode (or None of code is not valid"""
        if self.keycode in KeyBinder.ACCEPTED_KEYS: return self.keycode
        else: return None

class FolderPicker(tk.Button):
    """Button that, when pressed, prompts the user to select a folder"""
    folder_path: str
    def __init__(self,*args,**kwargs):
        super().__init__(command=self.folder_select,*args,**kwargs)
        #self.config(command=self.folder_select())
        self.folder_path = ""
        if "text" not in kwargs: self.config(text="Choose folder")
    def folder_select(self):
        self.folder_path = filedialog.askdirectory()
        title = self.folder_path
        if not title: title = "None"
        self.config(text=title)
    def get_folder_path(self) -> str | None:
        if path.exists(self.folder_path): return self.folder_path
        else: return None



class KeyDirAssociation(tk.Frame):
    """
    Frame with two buttons side by side, one for binding a key and
    one for binding a folder
    """
    def __init__(self,*args,**kwargs):
        super().__init__(*args,*kwargs)

        # grid configuration
        self.rowconfigure(0,weight=1)
        self.columnconfigure(0,weight=1)
        self.columnconfigure(1,weight=3)

        self.btn_key = KeyBinder(master=self)
        self.btn_key.grid(row=0,column=0)

        self.btn_folder = FolderPicker(master=self)
        self.btn_folder.grid(row=0,column=1)

    def get_values(self) -> tuple[str,str] | None:
        """Returns the key/folder pair"""
        key = self.btn_key.get_keycode()
        folder = self.btn_folder.get_folder_path()
        if key and folder: return key,folder
        else: return None

# TODO: create a new class that's a grid of KeyDirAssoc