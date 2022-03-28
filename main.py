from tkinter import *
from pydicom import *
from PIL import Image, ImageTk

root = Tk()
ds = dcmread("plik.dcm")
label = Label(text=str(ds))

img = ImageTk.PhotoImage(image=Image.fromarray(ds.pixel_array))

canvas = Canvas(root, width=512, height=512)
canvas.pack()
canvas.create_image(0, 0, anchor="nw", image=img)

label.pack()

root.mainloop()
