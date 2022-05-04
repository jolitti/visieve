from typing import Generator
from .datatypes import InstanceConfig, SieveMode, DuplicateMode
from .fileutil import count_image_files, is_valid_image_file, get_unique_filename
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import PIL
from PIL import Image, ImageTk
import os, sys
import shutil
from pathlib import Path
import ntpath

class SortingDialog:
    
    def __init__(self,config: InstanceConfig) -> None:
        # config assignment and validation
        self.config = config
        validity = self.config.is_valid()
        if validity is not True: raise ValueError(validity)
        if not self.config.are_destinations_empty():
            messagebox.showwarning(
                title="File warning",
                message="One or more destination directories are not empty. \
                        Those files may be overwritten during execution"
                )

        # counter and max assignment
        self.total_image_count = count_image_files(self.config.source)
        if self.total_image_count <= 0:
            print("No images found! Quitting")
            sys.exit()
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
        self._get_bindings_list().grid(row=0,column=1)

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
        dest_dir = self.config.dest.get(key)
        if dest_dir[-1] != "/": dest_dir+="/" # just to be sure to be able to concatenate
        filename = ntpath.basename(self.current_img_path)
        dest_name = dest_dir + filename

        # check if file with same name already exists at destination
        # if so, handle collision according to self.duplicate_mode
        if os.path.exists(dest_name):
            dest_name = self.solve_name_conflict(dest_name)

        # copy or move depending on configuration
        match self.config.sieve_mode:
            case SieveMode.COPY:
                shutil.copy2(self.current_img_path,dest_name)
                print(f"Copying {self.current_img_path} into {dest_dir}")
            case SieveMode.MOVE:
                shutil.copy2(self.current_img_path,dest_name)
                os.remove(self.current_img_path)
                print(f"Moving {self.current_img_path} into {dest_dir}")
            case _:
                raise ValueError(f"Sieve mode {self.config.sieve_mode} is not supported")

        self.update_image()

    def solve_name_conflict(self,destination:str) -> str | None:
        """
        To be called if the file at path destination exists to solve the collision.
        Will handle the existing file according to self.config and will return the final filename
        (or None if the file is not to be copied)
        """
        match self.config.duplicate_mode:
            case DuplicateMode.MAINTAIN:
                # the already existing file has precedence, do not copy
                return None
            case DuplicateMode.OVERWRITE:
                # the existing file must be deleted, use its name
                os.remove(destination)
                return destination
            case DuplicateMode.ASSIGN_UNIQUE_NAME:
                # preserve the old file, enumerate the new one until you get a unique name
                return get_unique_filename(destination)
            case DuplicateMode.HALT:
                # deliberarely crash the program
                raise ValueError("Error! File already exists and DuplicateMode is HALT")
            case _:
                # catch-all for invalid mode
                raise ValueError(f"Error! Invalid DuplicateMode: {self.config.duplicate_mode=}")

    def update_image(self):
        """Pass the next image in the generator to the label"""

        # update the progress bar
        self.progress_bar["value"] = self.counter/self.total_image_count * 100
        self.counter += 1

        # get the PhotoImage, path of the next file
        try:
            img,path= next(self.img_generator)
        except StopIteration as s:
            # a StopIteration gets thrown by a generator once it reaches the end
            print("Reached end of file set")
            sys.exit()

        # assign the file to the label and memorize the path for the move/copy operation
        self.lab_img.configure(image=img)
        self.lab_img.image = img # Prevents the garbage collector from deleting the img object
        self.current_img_path = path

    def images_iterator(self) -> Generator[tuple[ImageTk.PhotoImage,str],None,None]:
        """
        Generator of pairs of PhotoImage and its corresponding path and order in directory
        (sorted in chronological order, oldest first)
        """
        paths = sorted(Path(os.fsdecode(self.config.source)).iterdir(), key=os.path.getmtime, reverse=True)
        for p in paths:
            # skip this file if it's not an image
            if not is_valid_image_file(p): continue

            # open the file, resize it and return it as a PhotoImage
            with Image.open(p) as image_file:
                (a,b) = image_file.size
                width = self.config.size[0]
                new_size = (width,int(b*width/a))
                resized_image = image_file.resize(new_size,PIL.Image.BICUBIC)
            yield (ImageTk.PhotoImage(resized_image),p)

    def _get_bindings_list(self) -> tk.Frame:
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