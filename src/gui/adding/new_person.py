###########################################################################################
# -*- coding: utf-8 -*-
###########################################################################################
# Project: MeetingPro
# File: new_person.py
###########################################################################################
# Creation Date: 19-05-2025
# Authors: Lucas DAGON
# Description: This script creates the main window that can open all other windows.
###########################################################################################


import tkinter as tk
import os
import sys
from PIL import Image, ImageTk
from tkinter import ttk
from src.controller.add_client import add_client


class Add_Client:
    """ This class creates the window to add a new employee. """
    fullscreenstate = False
    
    def __init__(self, master):
        self.master = master
        self.master.grid()
        self.master.config(bg='black')
        self.master.title("Ajouter un client")
        self.master.geometry('1920x1080')
        self.master.resizable(1,1)
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)

        self.background_image()

        self.frame = ttk.Frame(self.master)
        self.text_box_surname = tk.Text(self.frame, width=1, height=10, relief='groove', wrap='word', borderwidth=5)
        self.text_box_surname.grid(row=0, column=0, padx=10, pady=10)
        self.text_box_name = tk.Text(self.frame, height=1, width=10)
        self.text_box_name.grid(row=1, column=0, padx=10, pady=10)
        self.text_box_email = tk.Text(self.frame, height=1, width=10)
        self.text_box_email.grid(row=2, column=0, padx=10, pady=10)
        self.add_new_client = ttk.Button(self.frame, text='Ajouter un nouveau client', width=25, command=self.create_client)
        self.add_new_client.grid(row=3, column=1, padx=10, pady=10)
        self.frame.pack()

    def create_client(self):
        self.get_strings()
        print(f"Creating client with name: {self.name}, surname: {self.surname}, email: {self.email}")

    def get_strings(self):
        self.surname = self.text_box_surname.get("1.0", "end-1c")
        self.name = self.text_box_name.get("1.0", "end-1c")
        self.email = self.text_box_email.get("1.0", "end-1c")
        print(self.surname)
        print(self.name)
        print(self.email)

    def background_image(self)-> None:
        #BG image
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

    def toggle_fullscreen(self, event=None):
        self.fullscreenstate = not self.fullscreenstate  # Just toggling the boolean
        self.master.attributes("-fullscreen", self.fullscreenstate)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreenstate = False
        self.master.attributes("-fullscreen", False)
        return "break"