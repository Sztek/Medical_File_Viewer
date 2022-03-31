from tkinter import *
from pydicom import *
import glob
# from pydicom.data import get_testdata_file
from pydicom.fileset import FileSet
from PIL import Image, ImageTk


class Plotno:
    warstwa = 0
    canvas = 0
    instance = 0
    img = 0

    def tick(self, event):
        self.warstwa += int(event.delta/(-120))
        if self.warstwa > len(self.instance)-1:
            self.warstwa = len(self.instance)-1
        if self.warstwa < 0:
            self.warstwa = 0
        # print(self.warstwa)
        self.draw()

    def create(self, root, instance):
        self.canvas = Canvas(root, width=520, height=512)
        self.canvas.pack()
        self.canvas.bind('<MouseWheel>', self.tick)
        self.instance = instance

    def draw(self):
        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.instance[self.warstwa].load().pixel_array))
        self.canvas.create_image(0, 0, anchor="nw", image=self.img)
        self.canvas.create_rectangle(512, 0, 520, 512, fill='white', outline='')
        self.canvas.create_rectangle(512, self.warstwa*502/200, 520, self.warstwa*502/200+10, fill='black', outline='')


pole = Plotno()
root = Tk()

fs = FileSet()
for file in glob.glob('pliki/*.dcm'):
    ds = dcmread(file)
    fs.add(ds)
# print(fs)
instance = fs.find()

pole.create(root, instance)
pole.draw()

root.mainloop()
