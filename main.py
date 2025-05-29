#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: main.py
#################################################################
# Created Date: 2025-04-23
# Authors: DAGON Lucas, GRIMM--KEMPF Matthieu
# Description: Main entry point for the MeetingPro application.
#################################################################

# Import necessary modules
import tkinter as tk
from src.gui.main_gui import Main_Window
import os
import sys

def main():
    root = tk.Tk()
    app = Main_Window(root)
    root.mainloop()

if __name__ == "__main__":
    main()