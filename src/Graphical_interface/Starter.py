###########################################################################################
#-*- coding: utf-8 -*-                                                                    #
###########################################################################################
# This is a simple GUI application using Tkinter in Python.                               #
# By: Lucas DAGON                                                                         #
# Date: 23-04-25                                                                          #
# file: Starter.py                                                                        #
# Description: This script creates a basic window with a label and a button, for now.     #
###########################################################################################

import tkinter as tk
import tkcalendar
import os
import sys
from PIL import Image, ImageTk
from tkinter import ttk



class Main_Window:
    def __init__(self, master, path_to_image:str):
        self.master = master
        self.master.grid()
        self.master.config(bg='black')
        self.master.title("test")
        self.master.geometry('520x300')
        self.master.resizable(1,1)
        self.frame = ttk.Frame(self.master)
        self.button1 = ttk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window).grid(row=0, column=0, padx=10, pady=10)
        self.button_calendar = ttk.Button(self.frame, text = 'New Window', width = 10, command = self.open_calendar).grid(row=1, column=0, padx=10, pady=10)
        
        self.path_to_image:str = path_to_image
        self.image = Image.open(path_to_image)
        self.image = ImageTk.PhotoImage(self.image)

        # Create a label to display the image
        image_label = tk.Label(self.master, image=self.image).grid(row=0, column=2, padx=10, pady=10)
        self.image_label.pack()

        self.frame.pack()

    def open_calendar(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Create_Calendar(self.newWindow)

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

class Create_Calendar:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.calendar = tkcalendar.Calendar(self.master, selectmode='day', year=2023, month=4, day=25)
        self.calendar.pack(pady=20)
        self.frame.pack()

class Demo2:
    def __init__(self, master):
        self.master = master
        self.frame = ttk.Frame(self.master)
        self.quitButton = ttk.Button(self.frame, text = 'Quit', width = 25, command = self.close_windows)
        self.quitButton.pack()
        self.frame.pack()
        
    def close_windows(self):
        self.master.destroy()

def main(): 
    os.chdir(sys.path[0])
    path_to_image = "test.png"
    full_path:str = os.path.join(os.getcwd(), path_to_image)
    root = tk.Tk()
    app = Main_Window(root, full_path)
    root.mainloop()

if __name__ == '__main__':
    main()