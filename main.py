from tkinter import *
from pydicom import *
import glob, os
# from pydicom.data import get_testdata_file
from pydicom.fileset import FileSet
from PIL import Image, ImageTk
from math import sqrt


def load(name):
    fs = FileSet()
    if os.path.isdir(name):
        for file in glob.glob(name+'/*.dcm'):
            ds = dcmread(file)
            fs.add(ds)
    return fs.find()


class Plotno:
    def __init__(self, root):
        self.warstwa = 0
        self.size = 512
        self.canvas = Canvas
        self.instance = FileSet
        self.img = ImageTk
        self.canvas = Canvas(root, width=520, height=512)

        self.canvas.bind('<MouseWheel>', self.tick)

    def tick(self, event):
        self.warstwa += int(event.delta/(-120))
        if self.warstwa > len(self.instance)-1:
            self.warstwa = len(self.instance)-1
        if self.warstwa < 0:
            self.warstwa = 0
        # print(self.warstwa)
        self.draw()

    def set(self, instance):
        if instance:
            self.instance = instance
            self.warstwa = 0
            self.size = (sqrt(instance[0].load().pixel_array.size))
            self.canvas.pack()
            self.draw()

    def draw(self):
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.instance[self.warstwa].load().pixel_array))
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.create_rectangle(512, 0, 520, 512, fill='white', outline='')
        self.canvas.create_rectangle(512, self.warstwa*502/200, 520, self.warstwa*502/200+10, fill='black', outline='')


root = Tk()
pole = Plotno(root)

menu = Frame(root)
menu.pack()

title = Label(menu, text='DICOM Viewer', font=('Arial', 20))
title.pack()

name = Entry(menu)
name.pack()

button = Button(menu, text='load', command=lambda: pole.set(load(name.get())))
button.pack()

root.mainloop()
