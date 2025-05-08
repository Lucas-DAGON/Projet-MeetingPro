import tkinter as tk
import tkcalendar
from tkinter import ttk
import os
import sys
from PIL import Image, ImageTk

class Create_Calendar:
    """This class creates a calendar using the tkcalendar library."""
    fullscreenstate = False

    def __init__(self, master):
        self.master = master
        self.master.geometry('1920x1080')
        self.master.grid()
        self.master.config(bg='black')
        self.master.title("test")
        self.master.resizable(1,1)
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)

        self.background_image()

        self.calendar = tkcalendar.Calendar(self.master, selectmode='day', year=2023, month=4, day=25)
        self.calendar.pack(fill="both", expand=True)

        self.frame = ttk.Frame(self.master)
        self.button_quit = ttk.Button(self.frame, text = 'Quit', width = 20, command = self.close_windows).grid(row=1, column=0, padx=10, pady=10)
        
        self.frame.pack()
        return
    
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