# import time
# import threading
# from PIL import Image, ImageTk, ImageSequence
# import PySimpleGUI as sg
# from PySimpleGUI.PySimpleGUI import PopupNoBorder
# from AI.SpeakAndListen import get_audio
#
#
#
# class animation():
#     def __init__(self, animation_type):
#         # threading.Thread.__init__(self)
#         if animation_type=="recognization":
#             self.bear = 'Images/recognization.gif'
#         else:
#             self.bear = 'Images/listening.gif'
#
#         self.stop = False
#
#     def run(self):
#         layout = [[sg.Image(key='-IMAGE-')]]
#
#         window = sg.Window('Window Title', layout,size=(300, 200),  element_justification='c', margins=(0,0), element_padding=(0,0), finalize=True, no_titlebar=True)
#
#         sequence = [ImageTk.PhotoImage(img) for img in ImageSequence.Iterator(Image.open(self.bear))]
#
#         interframe_duration = Image.open(self.bear).info['duration']
#
#         while True:
#             for frame in sequence:
#                 event, values = window.read(timeout=interframe_duration)
#                 if event == sg.WIN_CLOSED or self.stop:
#                     exit()
#                 window['-IMAGE-'].update(data=frame)
#
#     def stops(self):
#         self.stop=True


import tkinter as tk
from PIL import Image, ImageTk
from itertools import count
from tkinter.ttk import *
from tkinter import messagebox
import cv2
# from keyboard import wait

class ImageLabel(tk.Label):

    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        self.loc = 0
        self.frames = []

        try:
            for i in count(1):
                self.frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(self.frames) == 1:
            self.config(image=self.frames[0])
        else:
            self.next_frame()

    def unload(self):
        self.config(image="")
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.loc += 1
            self.loc %= len(self.frames)
            self.config(image=self.frames[self.loc])
            self.after(self.delay, self.next_frame)


def run():

    root = tk.Tk()

    def hel():

        print(help(cv2))


    def Contri():

        tk.messagebox.showinfo("Contributors", "\n1.Muhammad Khan \n2. Kamran Fiaz \n")


    def anotherWin():

        tk.messagebox.showinfo("About",
                                    ' Virtual Assistace version v1.0\n Made by Muhammad Khan & Kamran Fiaz \n FYP Project\n Made Using\n-OpenCV\n-Numpy\n-Tkinter\n-PySimpleGUI\n-PyWinHook\n In Python 3')


    def cont():
        tk.messagebox.showinfo("Contact Us",' For any Help\n kakarzai96@gmail.com ')


    menu = tk.Menu(root)
    root.config(menu=menu)

    subm1 = tk.Menu(menu)
    menu.add_cascade(label="Tools", menu=subm1)
    subm1.add_command(label="FYP Project ")

    subm2 = tk.Menu(menu)
    menu.add_cascade(label="About", menu=subm2)
    subm2.add_command(label="Driver Cam", command=anotherWin)
    subm2.add_command(label="Contributors", command=Contri)

    subm3 = tk.Menu(menu)
    menu.add_cascade(label="Help" , menu=subm3)
    subm3.add_command(label="Contact Us",command=cont)

    photo = tk.PhotoImage(file = "./AI/Images/start.png")

    photoimage = photo.subsample(10, 10)

    load = Image.open("./AI/Images/bg.jpg")
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.image = render
    img.place(x=0, y=0)
    def close():
        exit()

    root.geometry("900x500")
    root.protocol('WM_DELETE_WINDOW', close)
    # lbl = ImageLabel(root)
    # lbl.pack()
    # lbl.load('./AI/Images/listening1.gif')
    tk.Button(root, text = 'Start' , image = photoimage, command=root.destroy, width = 100 , bg= "#9604d5", bd= None,
                      relief="groove"  , compound = "left").place(x=390,y=335)
    root.mainloop()
    return True


