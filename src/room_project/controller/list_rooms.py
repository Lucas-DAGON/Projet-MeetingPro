#################################################################
# Project: MeetingPro
# File: list_reservations.py
#################################################################
# Created Date: 2025-05-27
# Authors: GRIMM--KEMPF Matthieu
# Description: Functions to list all rooms
#################################################################

# Imports
from json import loads
from os import path, listdir
from pathlib import Path

# Constants
ROOM_DIR = path.join(Path(__file__).parent.parent.parent, "room")


def list_rooms():
    """
    Function to list all rooms in the database
    :return: List of rooms
    """
    rooms = []
    # Verify if the rooms directory exists
    if not path.exists(ROOM_DIR):
        return rooms  # Return empty list if directory does not exist
    for filename in listdir(ROOM_DIR):
        # open each file and load the full name and id
        with open(path.join(ROOM_DIR, filename), "r") as f:
            data = loads(f.read())
            room = {
                "name": data["name"],
                "capacity": data["capacity"],
                "type": data["type"],
            }
            # Add the room to the list
            rooms.append(room)
    # Sort the list of rooms by full name
    rooms.sort(key=lambda x: x["name"])
    # Return the list of clients
    return rooms
