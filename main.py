from tkinter import *
from pydicom import *
import glob
import os
# from pydicom.data import get_testdata_file
# from pydicom.fileset import FileSet
from PIL import Image, ImageTk
from math import sqrt
from numpy import swapaxes


def load(name):
    # fs = FileSet()
    pixels = []
    if os.path.isdir(name):
        for file in glob.glob(name+'/*.dcm'):
            ds = dcmread(file)
            # fs.add(ds)
            pixels.append(ds.pixel_array)
    # return fs.find()
    return pixels


def transform(pixels):
    new_pixels = swapaxes(pixels, 0, 1)

    return new_pixels


class Plotno:
    def __init__(self, root):
        self.skala = 1
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
        #self.canvas.grid(row=0, column=1)


    def tick(self, event):
        self.warstwa += int(event.delta/(-120))
        if self.warstwa > len(self.pixels)-1:
            self.warstwa = len(self.pixels)-1
        if self.warstwa < 0:
            self.warstwa = 0
        # print(self.warstwa)
        self.draw()
        self.draw_side()

    def side_tick(self, event):
        self.warstwa_s = (self.canvas.winfo_pointerx() - self.canvas.winfo_rootx())
        if self.warstwa_s >= 512:
            self.warstwa_s = 511
        self.warstwa_b = (self.canvas.winfo_pointery() - self.canvas.winfo_rooty())
        if self.warstwa_b >= 512:
            self.warstwa_b = 511
        self.draw_side()

    def set(self, pixels):
        if True:
            # print(len(pixels[0]))
            # print(pixels[1][1][1])

            self.pixels = pixels
            self.pixels_s = swapaxes(self.pixels, 0, 2)
            self.pixels_b = swapaxes(self.pixels, 0, 1)
            sze = len(self.pixels) + len(self.pixels_b) + 8
            wys = len(self.pixels) + len(self.pixels_s) + 8
            if root.winfo_height() < wys:
                self.skala = root.winfo_height()/wys
            self.canvas = Canvas(width=sze*self.skala, height=wys*self.skala)
            self.warstwa = 0
            self.size = (sqrt(len(pixels[0])-1))
            self.canvas.pack(side='right', padx=10, pady=10)
            # self.canvas.grid(row=0, column=1)
            self.img = ImageTk.PhotoImage(image=Image.fromarray(self.pixels[self.warstwa]))
            self.draw_side()
            self.canvas.bind('<MouseWheel>', self.tick)
            self.canvas.bind('<Motion>', self.side_tick)
            print(root.winfo_height())

    def draw(self):
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.pixels[self.warstwa]))
        self.redraw()
        # self.canvas.create_rectangle(512, 0, 520, 512, fill='white', outline='')
        # self.canvas.create_rectangle(512,self.warstwa*502/200,520,self.warstwa*502/200+10,fill='black',outline='')
        # self.draw_side()

    def draw_side(self):
        self.img_s = ImageTk.PhotoImage(image=Image.fromarray(self.pixels_s[self.warstwa_s]))
        self.img_b = ImageTk.PhotoImage(image=Image.fromarray(self.pixels_b[self.warstwa_b]))
        self.redraw()
        self.canvas.create_rectangle(self.warstwa_s*self.skala, 0, self.warstwa_s*self.skala+1, 512*self.skala, fill='red', outline='')
        self.canvas.create_rectangle(0, self.warstwa_b*self.skala, 512*self.skala, self.warstwa_b*self.skala + 1, fill='blue', outline='')

    def redraw(self):
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.create_image(520*self.skala, 0, anchor="nw", image=self.img_s)
        self.canvas.create_image(0, 520*self.skala, anchor="nw", image=self.img_b)


root = Tk()
root.state("zoomed")

pole = Plotno(root)

menu = Frame(root, bg='azure', height=1000)
print(root.winfo_screenheight())
# menu.grid(row=0, column=0, ipadx=50, ipady=50)
menu.pack(side='left', padx=20, pady=20)

title = Label(menu, text='DICOM Viewer', font=('Arial', 10))
title.pack()

name = Entry(menu)
name.pack()

button = Button(menu, text='load', command=lambda: pole.set(load(name.get())))
button.pack()
root.mainloop()
