from tkinter import *
from tkinter import filedialog as fd
from pydicom import *
import glob
import os
from PIL import Image, ImageTk, ImageEnhance
from math import sqrt
from numpy import swapaxes


def load(path):
    pixels = []
    if os.path.isdir(path):
        for file in glob.glob(path + '/*.dcm'):
            ds = dcmread(file)
            pixels.append(ds.pixel_array)
    return pixels


class Plotno:
    def __init__(self):
        self.warstwa = 0
        self.warstwa_s = 0
        self.warstwa_b = 0
        self.size = 512
        self.pixels = []
        self.pixels_s = []
        self.pixels_b = []
        self.img = ImageTk
        self.img_s = ImageTk
        self.img_b = ImageTk
        self.canvas = Canvas(root)
        self.clicked = False
        self.hidden = False
        self.display = "I;16"

    def set(self, pixels):
        self.canvas.destroy()
        self.warstwa = 0
        self.warstwa_s = 0
        self.warstwa_b = 0
        if len(pixels) > 0:
            self.pixels = pixels
            self.pixels_s = swapaxes(self.pixels, 0, 2)
            self.pixels_b = swapaxes(self.pixels, 0, 1)
            sze = len(self.pixels) + len(self.pixels_b) + 8
            wys = len(self.pixels) + len(self.pixels_s) + 8
            self.canvas = Canvas(root, width=sze, height=wys)
            self.warstwa = 0
            self.size = (sqrt(len(pixels[0])-1))
            self.canvas.pack(side='right', padx=10, pady=10)
            self.draw()
            self.canvas.bind('<MouseWheel>', self.scroll_tick)
            self.canvas.bind('<Motion>', self.move_tick)
            self.canvas.bind('<Button-1>', self.onclick)

    def scroll_tick(self, event):
        self.warstwa += int(event.delta/(-120))
        if self.warstwa > len(self.pixels)-1:
            self.warstwa = len(self.pixels)-1
        if self.warstwa < 0:
            self.warstwa = 0
        self.draw()

    def move_tick(self, event):
        if not self.clicked:
            self.warstwa_s = (self.canvas.winfo_pointerx() - self.canvas.winfo_rootx())
            if self.warstwa_s >= 512:
                self.warstwa_s = 511
            self.warstwa_b = (self.canvas.winfo_pointery() - self.canvas.winfo_rooty())
            if self.warstwa_b >= 512:
                self.warstwa_b = 511
        self.draw()

    def draw(self):
        self.canvas.delete('all')
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.pixels[self.warstwa], mode=self.display))
        self.img_s = ImageTk.PhotoImage(image=Image.fromarray(self.pixels_s[self.warstwa_s], mode=self.display))
        self.img_b = ImageTk.PhotoImage(image=Image.fromarray(self.pixels_b[self.warstwa_b], mode=self.display))
        if not self.hidden:
            self.canvas.create_rectangle(0, 520-1, 511, 520+200, outline='blue')
            self.canvas.create_rectangle(520-1, 0, 520+200, 511, outline='red')
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.create_image(520, 0, anchor="nw", image=self.img_s)
        self.canvas.create_image(0, 520, anchor="nw", image=self.img_b)
        if not self.hidden:
            self.canvas.create_rectangle(self.warstwa_s, 0, self.warstwa_s+1, 512, fill='red', outline='')
            self.canvas.create_rectangle(0, self.warstwa_b, 512, self.warstwa_b+1, fill='blue', outline='')

    def onclick(self, event):
        if self.clicked:
            self.clicked = False
            self.move_tick(event)
        else:
            self.clicked = True

    def hide(self):
        if self.hidden:
            self.hidden = False
        else:
            self.hidden = True
        self.draw()

    def change(self):
        if self.display == "I;16":
            self.display = "LA"
        else:
            self.display = "I;16"
        self.draw()


root = Tk()
root.state('zoomed')
root.title('DICOM Viewer')

pole = Plotno()

menu = Frame(root)
menu.pack(side='left', padx=20, pady=20)

title = Label(menu, text='DICOM Viewer', font=('Arial', 20))
title.pack()

button = Button(menu, text='Select Directory', command=lambda: pole.set(load(fd.askdirectory())))
button.pack()
hide = Button(menu, text='hide axis', command=pole.hide)
hide.pack()
change = Button(menu, text='change display mode', command=pole.change)
change.pack()

root.mainloop()
