import imp
from typing import Generator
from .datatypes import InstanceConfig, SieveMode
from .fileutil import count_image_files, is_valid_image_file
import tkinter as tk
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
import os, sys
import shutil
from pathlib import Path

class SortingDialog:
    
    def __init__(self,config: InstanceConfig) -> None:
        # config assignment and validation
        self.config = config
        validity = self.config.is_valid()
        if validity is not True: raise ValueError(validity)

        # counter and max assignment
        self.total_image_count = count_image_files(self.config.source)
        self.counter = 0 # counts how many images have been processed

        # base window configuration
        self.window = tk.Tk()
        self.window.title("Visieve: Sorting window")
        self.window.rowconfigure(0,weight=5,minsize=self.config.size[1]*4/5) # main row
        self.window.rowconfigure(1,weight=1,minsize=self.config.size[1]*0.1) # progbar row
        self.window.columnconfigure(0,weight=2,minsize=self.config.size[0]*2/3) # image col
        self.window.columnconfigure(1,weight=1,minsize=self.config.size[0]/3) # legend col

        # set up image object generator to iterate through the media
        self.img_generator = self.images_iterator()
        
        # set up Label to house the image
        self.lab_img = tk.Label()
        self.lab_img.image = None
        self.lab_img.grid(row=0,column=0)
        # set up legend
        self._bindings_list().grid(row=0,column=1)

        # set up progress bar
        self.progress_bar = ttk.Progressbar(self.window,length=self.config.size[0])
        self.progress_bar.grid(row=1,column=0,columnspan=2)

        # create the bindings
        for (k,_) in self.config.dest.items():
            self.window.bind(k,self.handle_keypress)

        self.window.eval("tk::PlaceWindow . center")
        self.update_image()
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

        self.progress_bar["value"] = self.counter/self.total_image_count * 100
        self.counter += 1

        try:
            img,path,index = next(self.img_generator)
        except StopIteration as s:
            print("Reached end of file set")
            img,path,index = None,None,None

        if img is None:
            sys.exit()

        self.lab_img.configure(image=img)
        self.lab_img.image = img # Prevents the garbage collector from deleting the img object
        self.current_img_path = path

    def images_iterator(self) -> Generator[tuple[ImageTk.PhotoImage,str,int],None,None]:
        """
        Generator of pairs of PhotoImage and its corresponding path and order in directory
        (sorted in chronological order, oldest first)
        """
        index = 0
        paths = sorted(Path(os.fsdecode(self.config.source)).iterdir(), key=os.path.getmtime, reverse=True)
        for p in paths:
            with Image.open(p) as image_file:
                (a,b) = image_file.size
                width = self.config.size[0]
                new_size = (width,int(b*width/a))
                resized_image = image_file.resize(new_size,PIL.Image.BICUBIC)
            yield (ImageTk.PhotoImage(resized_image),p,index)
            index += 1

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