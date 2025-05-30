#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: cli.py
#################################################################
# Created Date: 2025-04-23
# Authors: DAGON Lucas, GRIMM--KEMPF Matthieu
# Description: Main entry point for the MeetingPro application.
#################################################################

# Import necessary modules
import tkinter as tk
from .gui.main_gui import Main_Window
import typer

application = typer.Typer()


@application.command()
def room_project(
    help: bool = typer.Option(
        False,
        "--help",
        "-h",
        help="Display the help message for the MeetingPro application.",
    ),
):
    """Manage room reservations."""
    if help:
        typer.echo(
            "MeetingPro is a meeting room management application. "
            "Use the GUI to manage rooms, clients, and reservations."
        )
    else:
        # Show the main GUI
        typer.echo("Starting the MeetingPro application...")
        root = tk.Tk()
        app = Main_Window(root)
        root.mainloop()


if __name__ == "__main__":
    application()
