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
from tkinter import ttk

class Main_Window:
    def __init__(self, master):
        self.master = master
        self.master.config(bg='black')
        self.master.title("test")
        self.master.geometry('520x300')
        self.master.resizable(1,1)
        self.frame = ttk.Frame(self.master)
        self.button1 = ttk.Button(self.frame, text = 'New Window', width = 25, command = self.new_window)
        self.button1.pack()
        self.frame.pack()

    def new_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Demo2(self.newWindow)

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
    root = tk.Tk()
    app = Main_Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()