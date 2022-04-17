from tkinter import *
from tkvideo import tkvideo

def_size = (700,500)

# create instance fo window
root = Tk()
root.geometry("700x500")
# set window title
root.title('Video Player')
# create label
Label(text="Space lore").pack()
video_label = Label(root)
video_label.pack()
# read video to display on label
player = tkvideo("example/afreightdata/afreightc.avi", video_label,
                 loop = 1, size = def_size)
player.play()
root.mainloop()