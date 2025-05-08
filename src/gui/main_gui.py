###########################################################################################
# -*- coding: utf-8 -*-
###########################################################################################
# Project: MeetingPro
# File: main_window.py
###########################################################################################
# Creation Date: 23-04-2025
# Authors: Lucas DAGON
# Description: This script creates the main window that can open all other windows.
###########################################################################################

import tkinter as tk
import os
import sys
from PIL import Image, ImageTk
from tkinter import ttk
# Debuging
if __name__ == "__main__":
    from login import Login_Account, Create_Account
    from create_calendar import Create_Calendar
else:
    from src.gui.login import Login_Account, Create_Account
    from src.gui.create_calendar import Create_Calendar





class Main_Window:
    """ Creates the main window of the application. """
    fullscreenstate = False
    def __init__(self, master):
        self.master = master
        
        self.master.grid()
        self.master.config(bg='black')
        self.master.title("test")
        self.master.geometry('1920x1080')
        self.master.resizable(1,1)
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)

        self.background_image()
        
        self.frame = ttk.Frame(self.master)
        self.button_login = ttk.Button(self.frame, text = 'Login', width = 20, command = self.login_window).grid(row=5, column=1, padx=10, pady=10)
        self.button_create_account = ttk.Button(self.frame, text = 'Create Account', width = 20, command = self.create_account_window).grid(row=6, column=1, padx=10, pady=10)
        self.button_calendar = ttk.Button(self.frame, text = 'Open Calendar', width = 20, command = self.open_calendar).grid(row=5, column=0, padx=10, pady=10)
        self.button_quit = ttk.Button(self.frame, text = 'Quit', width = 20, command = self.close_windows).grid(row=6, column=0, padx=10, pady=10)
        self.frame.pack()

    def open_calendar(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Create_Calendar(self.newWindow)

    def login_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Login_Account(self.newWindow)

    def create_account_window(self):
        self.newWindow = tk.Toplevel(self.master)
        self.app = Create_Account(self.newWindow)

    def background_image(self)-> None:
        """This function creates the background image of the gui."""
        #BG base path
        os.chdir(sys.path[0])

        # Change the path to the background image
        # Debugging
        if __name__ == "__main__":
            self.path_to_bg = "BG.jpg"
        else:
            self.path_to_bg = "src/gui/BG.jpg"

        self.full_path_to_bg:str = os.path.join(os.getcwd(), self.path_to_bg)
        self.image = Image.open(self.full_path_to_bg)
        self.image = ImageTk.PhotoImage(self.image, master = self.master)

        # Create a label to display the image
        self.image_label = tk.Label(self.master, image = self.image)
        self.image_label.place(x = 0, y = 0)

    def close_windows(self):
        self.master.destroy()

    def toggle_fullscreen(self, event=None):
        self.fullscreenstate = not self.fullscreenstate  # Just toggling the boolean
        self.master.attributes("-fullscreen", self.fullscreenstate)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreenstate = False
        self.master.attributes("-fullscreen", False)
        return "break"
   



def main(): 
    root = tk.Tk()
    app = Main_Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()