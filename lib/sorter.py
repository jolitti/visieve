import random
from typing import Generator
from .datatypes import InstanceConfig
import tkinter as tk
import PIL
from PIL import Image, ImageTk
import os
import shutil
from pathlib import Path

class SortingDialog:
    
    def __init__(self,config: InstanceConfig) -> None:
        self.config = config
        if not self.config.is_valid(): raise ValueError("Invalid configuration!")
        self.window = tk.Tk()
        self.window.geometry("600x600")
        self.img_generator = self.images_iterator()

        self.lab_img = tk.Label()
        self.lab_img.pack()

        self.update_image()
        for (k,i) in self.config.dest.items():
            self.window.bind(k,self.handle_keypress)

        self.window.mainloop()

    def handle_keypress(self,event:tk.Event):
        key = event.keysym
        if key not in self.config.dest: raise ValueError("Error: key bound but not in destination config")
        destination = self.config.dest.get(key)
        shutil.copy2(self.current_img_path,destination)
        print(f"Copying into {destination}")
        self.update_image()

    def update_image(self):
        """Pass the next image in the generator to the label"""
        (img,path) = next(self.img_generator)
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


def open_sorting_window(config: InstanceConfig):
    """Show the user a media sieving dialog"""
    SortingDialog(config)