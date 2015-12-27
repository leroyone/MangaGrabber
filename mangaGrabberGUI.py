#!/usr/bin/python

import Tkinter
import mymangaonlineGrabber
from PIL import Image, ImageTk
import io
from urllib2 import urlopen


class grabberGUI(Tkinter.Tk):
    def __init__(self,parent):
        Tkinter.Tk.__init__(self,parent)
        self.parent = parent
        self.geometry('317x415+422+195')
        self.initialize()

    def initialize(self):
        self.grid()

        self.entryVariable = Tkinter.StringVar()
        self.entry = Tkinter.Entry(self,textvariable=self.entryVariable)
        self.entry.grid(row=0, column=1, columnspan=2)
        self.entry.bind('<Return>', self.onPressEnter)
        self.entryVariable.set(u'Search for manga')
        
        ########## Button ##############
        
        button = Tkinter.Button(self,text=u"Search", command=self.onButtonClick)
        button.grid(row=0,column=1)
        
        ########### Label??? ###########
        
        self.labelVariable = Tkinter.StringVar()
        label = Tkinter.Label(self,textvariable=self.labelVariable,fg='black',bg='white')
        label.grid(row=1,column=1,columnspan=3)
        self.labelVariable.set(u'hello')

        self.grid_columnconfigure(0,weight=1)
        self.resizable(True,True)
        self.update()
        self.geometry(self.geometry())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
        self.printImage("http://images.mymangaonline.com/images/death-note/death-note.jpg", 2, 0)
        self.printImage("http://images.mymangaonline.com/images/dragon-ball-heroes-victory-mission/dragon-ball-heroes-victory-mission.jpg", 2, 1)
        self.printImage("http://images.mymangaonline.com/images/death-note/death-note.jpg", 2, 2)

        ############# Image test ###########
    def printImage(self,imageLink,rowNumber, colNumber):
        image_bytes = urlopen(imageLink).read()
        data_stream = io.BytesIO(image_bytes)
        pil_image = Image.open(data_stream)
        baseheight = 200
        wpercent = (baseheight/float(pil_image.size[1]))
        wsize = int((float(pil_image.size[0])*float(wpercent)))
        resized = pil_image.resize((wsize,baseheight), Image.ANTIALIAS)
        tk_image = ImageTk.PhotoImage(resized)

        label0 = Tkinter.Label(self, image=tk_image)
        label0.grid(row=rowNumber, column=colNumber)
        label0.image = tk_image
        
    def onPressEnter(self, event):
        self.labelVariable.set(self.entryVariable.get())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)
        
    def onButtonClick(self):
        self.labelVariable.set(self.entryVariable.get())
        self.entry.focus_set()
        self.entry.selection_range(0, Tkinter.END)

if __name__ == "__main__":
    app = grabberGUI(None)
    app.title('Manga Grabber')
    app.mainloop()
    