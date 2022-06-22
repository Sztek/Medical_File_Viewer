from tkinter import *
from tkinter import filedialog as fd
from pydicom import *
import nibabel as nib
import glob
import os
from PIL import Image, ImageTk
from numpy import swapaxes, int16, eye


class Plik:
    def __init__(self):
        self.pixels = []
        self.affine = eye(4)
        self.header = nib.Nifti1Header()
        self.shape = 0

    def saveNifti(self):
        img = nib.Nifti1Image(self.pixels, self.affine, self.header)
        nib.save(img, 'clipped_image.nii')


class Dicom(Plik):
    def load(self, path):
        self.pixels = []
        if os.path.isdir(path):
            for file in glob.glob(path + '/*.dcm'):
                ds = dcmread(file)
                self.pixels.append(ds.pixel_array)
        self.affine = eye(4)
        self.pixels = int16(self.pixels)
        return self.pixels


class Nifti(Plik):
    def load(self, path):
        name = os.path.join(path.name)
        img = nib.load(name)
        self.pixels = img.get_fdata()
        self.affine = img.affine
        self.header = img.header
        return self.pixels


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

    def set(self, pixels):
        self.canvas.destroy()
        self.warstwa = 0
        self.warstwa_s = 0
        self.warstwa_b = 0
        if len(pixels) > 0:
            self.pixels = pixels
            self.pixels_s = swapaxes(self.pixels, 0, 2)
            self.pixels_b = swapaxes(self.pixels, 0, 1)
            sze = len(self.pixels) + len(self.pixels_s) + 8
            wys = len(self.pixels) + len(self.pixels_b) + 8
            self.canvas = Canvas(root, width=sze, height=wys)
            self.warstwa = 0
            self.canvas.pack(side='right', padx=10, pady=10)
            self.draw()
            self.canvas.bind('<Motion>', self.tick)
            self.canvas.bind('<ButtonPress-1>', self.onclick)
            self.canvas.bind('<ButtonRelease-1>', self.onrelease)

    def tick(self, event):
        x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        if self.clicked and x > 0 and y > 0:
            if x < len(self.pixels_s):
                self.warstwa_s = x
                if self.warstwa_s >= len(self.pixels_s):
                    self.warstwa_s = len(self.pixels_s)-1
            elif len(self.pixels_s) + 8 < x < len(self.pixels_s) + 8 + len(self.pixels):
                self.warstwa = x - len(self.pixels_s) - 8
            if y < len(self.pixels_b):
                self.warstwa_b = y
                if self.warstwa_b >= len(self.pixels_b):
                    self.warstwa_b = len(self.pixels_b)-1
            elif len(self.pixels_b) + 8 < y < len(self.pixels_b) + 8 + len(self.pixels):
                self.warstwa = y - len(self.pixels_b) - 8
        self.draw()

    def draw(self):
        red = len(self.pixels) + len(self.pixels_b) + 8
        blue = len(self.pixels) + len(self.pixels_s) + 8
        greenb = len(self.pixels_s)
        greenr = len(self.pixels_b)
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
            greenrpoz = len(self.pixels_s)+8+self.warstwa
            greenbpoz = len(self.pixels_b)+8+self.warstwa
            self.canvas.create_rectangle(self.warstwa_s, 0, self.warstwa_s + 1, red, fill='red', outline='')
            self.canvas.create_rectangle(0, self.warstwa_b, blue, self.warstwa_b + 1, fill='blue', outline='')
            self.canvas.create_rectangle(greenrpoz, 0, greenrpoz+1, greenr, fill='green', outline='')
            self.canvas.create_rectangle(0, greenbpoz, greenb, greenbpoz+1, fill='green', outline='')

    def onclick(self, event):
        self.clicked = True
        self.tick(event)

    def onrelease(self, event):
        self.clicked = False

    def hide(self):
        if self.hidden:
            self.hidden = False
        else:
            self.hidden = True
        self.draw()


root = Tk()
root.state('zoomed')
root.title('DICOM Viewer')

pole = Plotno()
dic = Dicom()
nif = Nifti()

menu = Frame(root)
menu.pack(side='left', padx=20, pady=20)

title = Label(menu, text='DICOM Viewer', font=('Arial', 20))
title.pack()

buttond = Button(menu, text='Select Dicom', command=lambda: pole.set(dic.load(fd.askdirectory())))
buttond.pack()

buttonn = Button(menu, text='Select Nifti', command=lambda: pole.set(nif.load(fd.askopenfile())))
buttonn.pack()

buttonx = Button(menu, text='save Nifti from DICOM', command=dic.saveNifti)
buttonx.pack()

buttonz = Button(menu, text='save Nifti from Nifti', command=nif.saveNifti)
buttonz.pack()

hide = Button(menu, text='hide axis', command=pole.hide)
hide.pack()


root.mainloop()
