import tkinter as tk
from PIL import Image, ImageTk
import os
import sys


def background_image(frame)-> None:
        """This function creates the background image of the gui."""
        # BG base path
        os.chdir(sys.path[0])

        # Change the path to the background image
        path_to_bg = "src/gui/BG.jpg"

        full_path_to_bg:str = os.path.join(os.getcwd(), path_to_bg)
        image = Image.open(full_path_to_bg)
        image = ImageTk.PhotoImage(image, master = frame)

        # Create a label to display the image
        image_label = tk.Label(frame, image = image)
        image_label.place(x=0, y=0, relwidth=1, relheight=1)
        image_label.image = image