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
    def __init__(self,*args,**kwargs):
        super().__init__(command=self.start_keybind,*args,**kwargs)
        #self.config(command=self.folder_select())
        self.keycode = None
        if "text" not in kwargs: self.config(text="Choose key")

    def start_keybind(self):
        """Alert the application to start listening to keypresses"""
        if self.keycode:
            self.winfo_toplevel().unbind(self.keycode)
        self.winfo_toplevel().bind("<Key>",self.bind_key)
        self.config(text="Press a key...")

    def bind_key(self,event:tk.Event):
        """Triggered after keypress, captures its code"""
        # If event is not a char or a valid char
        if not event.char or event.char not in KeyBinder.ACCEPTED_KEYS:
            self.keycode = None
            self.config(text="Choose key")
        else:
            self.keycode = event.keysym.lower()
            self.config(text=event.keysym)
            # if we do have a bind_list, add the new char to it
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



class KeyDirPair(tk.Frame):
    """
    Frame with two buttons side by side, one for binding a key and
    one for binding a folder
    """
    def __init__(self,master,*args,**kwargs):
        super().__init__(master,*args,*kwargs)

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


class KeyDirList(tk.Frame):

    pairs: list[KeyDirPair]
    """List that houses the KeyDirPair widgets"""

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.columnconfigure(0,weight=1)
        self.pairs = []
    
    def add_pair(self):
        """Append a new KeyDirPair under the existing ones"""
        index = len(self.pairs)
        newpair = KeyDirPair(self)
        self.rowconfigure(index,weight=1)
        newpair.grid(row=index,column=0)
        self.pairs.append(newpair)

    def remove_pair(self):
        """Remove the last KeyDirPair"""
        oldpair = self.pairs.pop()
        oldpair.grid_forget()

    def get_binding_pairs(self) -> dict[str,str]:
        """Returns the key-dir pairs (to be put into InstanceConfig)"""
        ans = dict()
        for pair in self.pairs:
            association = pair.get_values()
            if association is not None: 
                key,val = association
                ans[key] = val
        return ans

class CompleteKeyDirBinder(tk.Frame):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        for i in range(2):
            self.rowconfigure(i,weight=1)
            self.columnconfigure(i,weight=1)

        self.kdgrid = KeyDirList(self)
        self.btn_add = tk.Button(self,text="+",command=self.kdgrid.add_pair)
        self.btn_remove = tk.Button(self,text="-",command=self.kdgrid.remove_pair)

        # put in grid
        self.kdgrid.grid(row=0,column=0,columnspan=2)
        self.btn_add.grid(row=1,column=0)
        self.btn_remove.grid(row=1,column=1)
    
    def get_binding_pairs(self) -> dict[str,str]:
        return self.kdgrid.get_binding_pairs()