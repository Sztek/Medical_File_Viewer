from tkinter import *
from tkinter import filedialog as fd
from pydicom import *
import nibabel as nib
import glob
import os
from PIL import Image, ImageTk
from numpy import swapaxes


class Plotno:
    def __init__(self):
        self.warstwa = 0
        self.warstwa_s = 0
        self.warstwa_b = 0
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
            self.canvas.pack(side='right', padx=10, pady=10)
            self.draw()
            self.canvas.bind('<Motion>', self.move_tick)
            self.canvas.bind('<Button-1>', self.onclick)

    def move_tick(self, event):
        x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        if not self.clicked:
            if x < len(self.pixels_s):
                self.warstwa_s = x
                if self.warstwa_s >= len(self.pixels_s):
                    self.warstwa_s = len(self.pixels_s)-1
            elif len(self.pixels_s) + 8 < x < len(self.pixels_s) + 8 + len(self.pixels):
                self.warstwa = x - len(self.pixels_b) - 8
            if y < len(self.pixels_b):
                self.warstwa_b = y
                if self.warstwa_b >= len(self.pixels_b):
                    self.warstwa_b = len(self.pixels_b)-1
            elif len(self.pixels_b) + 8 < y < len(self.pixels_b) + 8 + len(self.pixels):
                self.warstwa = y - len(self.pixels_s) - 8
        self.draw()

    def draw(self):
        red = len(self.pixels) + len(self.pixels_b) + 8
        blue = len(self.pixels) + len(self.pixels_s) + 8
        self.canvas.delete('all')
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.pixels[self.warstwa]))
        self.img_s = ImageTk.PhotoImage(image=Image.fromarray(self.pixels_s[self.warstwa_s]))
        self.img_b = ImageTk.PhotoImage(image=Image.fromarray(self.pixels_b[self.warstwa_b]))
        if not self.hidden:
            self.canvas.create_rectangle(0, len(self.pixels_b)+7, len(self.pixels_s)-1, red, outline='blue')
            self.canvas.create_rectangle(len(self.pixels_s)+7, 0, blue, len(self.pixels_b)-1, outline='red')
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.create_image(len(self.pixels_s)+8, 0, anchor="nw", image=self.img_s)
        self.canvas.create_image(0, len(self.pixels_b)+8, anchor="nw", image=self.img_b)
        if not self.hidden:
            self.canvas.create_rectangle(self.warstwa_s, 0, self.warstwa_s + 1, red, fill='red', outline='')
            self.canvas.create_rectangle(0, self.warstwa_b, blue, self.warstwa_b + 1, fill='blue', outline='')

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

    def loadDicom(self, path):
        pixels = []
        if os.path.isdir(path):
            for file in glob.glob(path + '/*.dcm'):
                ds = dcmread(file)
                pixels.append(ds.pixel_array)
        return pixels

    def loadNifti(self, path):
        name = os.path.join(path.name)
        img = nib.load(name)
        pixels = img.get_fdata()
        return pixels


root = Tk()
root.state('zoomed')
root.title('DICOM Viewer')

pole = Plotno()

menu = Frame(root)
menu.pack(side='left', padx=20, pady=20)

title = Label(menu, text='DICOM Viewer', font=('Arial', 20))
title.pack()

buttond = Button(menu, text='Select Dicom', command=lambda: pole.set(pole.loadDicom(fd.askdirectory())))
buttond.pack()

buttonn = Button(menu, text='Select Nifti', command=lambda: pole.set(pole.loadNifti(fd.askopenfile())))
buttonn.pack()

hide = Button(menu, text='hide axis', command=pole.hide)
hide.pack()
change = Button(menu, text='change display mode', command=pole.change)
change.pack()


root.mainloop()
