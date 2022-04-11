from tkinter import *
from pydicom import *
import glob
import os
from PIL import Image, ImageTk
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

    def set(self, pixels):
        if len(pixels) > 0:
            self.pixels = pixels
            self.pixels_s = swapaxes(self.pixels, 0, 2)
            self.pixels_b = swapaxes(self.pixels, 0, 1)
            sze = len(self.pixels) + len(self.pixels_b) + 8
            wys = len(self.pixels) + len(self.pixels_s) + 8
            self.canvas = Canvas(width=sze, height=wys)
            self.warstwa = 0
            self.size = (sqrt(len(pixels[0])-1))
            self.canvas.pack(side='right', padx=10, pady=10)
            self.draw()
            self.canvas.bind('<MouseWheel>', self.tick)
            self.canvas.bind('<Motion>', self.side_tick)

    def tick(self, event):
        self.warstwa += int(event.delta/(-120))
        if self.warstwa > len(self.pixels)-1:
            self.warstwa = len(self.pixels)-1
        if self.warstwa < 0:
            self.warstwa = 0
        self.draw()

    def side_tick(self, event):
        self.warstwa_s = (self.canvas.winfo_pointerx() - self.canvas.winfo_rootx())
        if self.warstwa_s >= 512:
            self.warstwa_s = 511
        self.warstwa_b = (self.canvas.winfo_pointery() - self.canvas.winfo_rooty())
        if self.warstwa_b >= 512:
            self.warstwa_b = 511
        self.draw()

    def draw(self):
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.pixels[self.warstwa]))
        self.img_s = ImageTk.PhotoImage(image=Image.fromarray(self.pixels_s[self.warstwa_s]))
        self.img_b = ImageTk.PhotoImage(image=Image.fromarray(self.pixels_b[self.warstwa_b]))
        self.canvas.create_rectangle(0, 520-1, 511, 520+200, outline='blue')
        self.canvas.create_rectangle(520-1, 0, 520+200, 511, outline='red')

        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.create_image(520, 0, anchor="nw", image=self.img_s)
        self.canvas.create_image(0, 520, anchor="nw", image=self.img_b)

        self.canvas.create_rectangle(self.warstwa_s, 0, self.warstwa_s+1, 512, fill='red', outline='')
        self.canvas.create_rectangle(0, self.warstwa_b, 512, self.warstwa_b+1, fill='blue', outline='')


root = Tk()
root.state("zoomed")

pole = Plotno()

menu = Frame(root, bg='azure')
menu.pack(side='left', padx=20, pady=20)

title = Label(menu, text='DICOM Viewer', font=('Arial', 20))
title.pack()

name = Entry(menu)
name.pack()

button = Button(menu, text='load', command=lambda: pole.set(load(name.get())))
button.pack()
root.mainloop()
