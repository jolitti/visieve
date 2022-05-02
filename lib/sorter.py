from typing import Generator
from .datatypes import InstanceConfig, SieveMode
import tkinter as tk
import PIL
from PIL import Image, ImageTk
import os, sys
import shutil
from pathlib import Path

class SortingDialog:
    
    def __init__(self,config: InstanceConfig) -> None:
        self.config = config
        validity = self.config.is_valid()
        if validity is not True: raise ValueError(validity)

        #base window configuration
        self.window = tk.Tk()
        self.window.title("Visieve: Sorting window")
        self.window.rowconfigure(0,weight=1,minsize=self.config.size[1])
        self.window.columnconfigure(0,weight=2,minsize=self.config.size[0]*2/3)
        self.window.columnconfigure(1,weight=1,minsize=self.config.size[0]/3)

        # set up image object generator to iterate through the media
        self.img_generator = self.images_iterator()
        
        # set up Label to house the image
        self.lab_img = tk.Label()
        self.lab_img.grid(row=0,column=0)
        self.update_image()

        # set up legend
        self._bindings_list().grid(row=0,column=1)

        # create the bindings
        for (k,_) in self.config.dest.items():
            self.window.bind(k,self.handle_keypress)

        self.window.eval("tk::PlaceWindow . center")

        self.window.mainloop()

    def handle_keypress(self,event:tk.Event):
        """Function to be bound to the bound keys. Will move or copy the files as needed"""
        key = event.keysym
        if key not in self.config.dest: raise ValueError("Error: key bound but not in destination config")
        destination = self.config.dest.get(key)

        # copy or move depending on configuration
        match self.config.mode:
            case SieveMode.COPY:
                shutil.copy2(self.current_img_path,destination)
                print(f"Copying {self.current_img_path} into {destination}")
            case SieveMode.MOVE:
                shutil.copy2(self.current_img_path,destination)
                os.remove(self.current_img_path)
                print(f"Moving {self.current_img_path} into {destination}")
            case _:
                raise ValueError(f"Sieve mode {self.config.mode} is not supported")

        self.update_image()

    def update_image(self):
        """Pass the next image in the generator to the label"""
        
        try:
            img,path = next(self.img_generator)
        except StopIteration as s:
            print("Reached end of file set")
            img,path = None,None

        if img is None:
            sys.exit()

        self.lab_img.configure(image=img)
        self.lab_img.image = img # Prevents the garbage collector from deleting the img object
        self.current_img_path = path

    def images_iterator(self) -> Generator[tuple[ImageTk.PhotoImage,str],None,None]:
        """
        Generator of pairs of PhotoImage and its corresponding path
        (sorted in chronological order, oldest first)
        """
        paths = sorted(Path(os.fsdecode(self.config.source)).iterdir(), key=os.path.getmtime, reverse=True)
        for p in paths:
            image_file = Image.open(p)
            (a,b) = image_file.size
            width = self.config.size[0]
            new_size = (width,int(b*width/a))
            image_file = image_file.resize(new_size,PIL.Image.BICUBIC)
            yield (ImageTk.PhotoImage(image_file),p)

    def _bindings_list(self) -> tk.Frame:
        """Get a frame that contains a grid of labels showing the bindings"""
        frame = tk.Frame(master=self.window)
        
        # column responsiveness configuration
        frame.columnconfigure(0,weight=1) # key column
        frame.columnconfigure(0,weight=2) # folder column

        # rows generation + row responsiveness configuration
        for i,(key,folder) in enumerate(self.config.dest.items()):
            frame.rowconfigure(i,weight=1)
            tk.Label(master=frame,text=key,relief=tk.GROOVE,padx=10).grid(row=i,column=0) # key label
            tk.Label(master=frame,text=folder,relief=tk.GROOVE).grid(row=i,column=1) # key label

        return frame

    def _quit(self):
        self.window.destroy()


def open_sorting_window(config: InstanceConfig):
    """Show the user a media sieving dialog"""
    SortingDialog(config)