import tkinter as tk
from PIL import Image, ImageTk
from pathlib import Path


def background_image(frame) -> None:
    """This function creates the background image of the GUI."""

    # Get absolute path to the current file's directory
    current_dir = Path(__file__).resolve().parent

    # Build the full path to the image
    image_path = current_dir / "BG.jpg"

    # Open and display the image
    image = Image.open(image_path)
    image = ImageTk.PhotoImage(image, master=frame)

    image_label = tk.Label(frame, image=image)
    image_label.place(x=0, y=0, relwidth=1, relheight=1)
    image_label.image = image  # prevent garbage collection
