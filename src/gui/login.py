import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from src.calendar_logic.person import Person
import os
import sys


class Login_Account:
    """This class creates the login window of the application."""
    fullscreenstate = False

    def __init__(self, master):
        self.master = master
        self.master.grid()
        self.master.config(bg='black')
        self.master.title("Login")
        self.master.geometry('1920x1080')
        self.master.resizable(1,1)
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)

        self.background_image()

        self.frame = ttk.Frame(self.master)
        self.login = ttk.Button(self.frame, text = 'Login', width = 20, command = self.login_to_account).grid(row=0, column=0, padx=10, pady=10)
        self.button_quit = ttk.Button(self.frame, text = 'Quit', width = 20, command = self.close_windows).grid(row=1, column=0, padx=10, pady=10)
        self.frame.pack()
        
    def login_to_account(self):
        print("Login button clicked")

    def close_windows(self):
        self.master.destroy()

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






class Create_Account:
    """This class creates a new account for the user."""
    fullscreenstate = False

    def __init__(self, master):
        self.master = master
        self.master.grid()
        self.master.config(bg='black')
        self.master.title("Login")
        self.master.geometry('1920x1080')
        self.master.resizable(1,1)
        self.master.bind("<F11>", self.toggle_fullscreen)
        self.master.bind("<Escape>", self.end_fullscreen)

        self.background_image()

        self.frame = ttk.Frame(self.master)
        self.create_account = ttk.Button(self.frame, text = 'create an account', width = 25, command = self.create).grid(row=0, column=0, padx=10, pady=10)
        self.button_quit = ttk.Button(self.frame, text = 'Quit', width = 20, command = self.close_windows).grid(row=1, column=0, padx=10, pady=10)
        self.frame.pack()
        
    def create(self):
        # Test the person class
        person = Person("John Doe", "jone_doe@uha.fr")
        print(person)
        self.close_windows()

    def close_windows(self):
        self.master.destroy()

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


def main(): 
    root = tk.Tk()
    app = Create_Account(root)
    root.mainloop()

if __name__ == '__main__':
    main()