#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: return_room_object
#################################################################
# Created Date: 2025-05-31
# Authors: GRIMM--KEMPF Matthieu
# Description: Functions to return the object of a meeting rooms.
#################################################################

# Import necessary modules
from ..room_logic.standard import Standard
from ..room_logic.conference import Conference
from ..room_logic.computer import ComputerRoom


def return_room_object(name: str, type: str):
    """
    Function to return a room object from its name and type
    :param name: Name of the room
    :param type: Type of the room -> needed for the constructor
    """
    if type not in ["Standard", "Conference Room", "Computer Room"]:
        raise ValueError("Type must be standard, conference or computer")
    elif type == "Standard":
        room = Standard.load_from_json(name)
    elif type == "Conference Room":
        room = Conference.load_from_json(name)
    elif type == "Computer Room":
        room = ComputerRoom.load_from_json(name)
    else:
        raise ValueError(
            "Type must be standard, conference or computer"
        )  # This line is redundant due to the previous check, but kept for clarity.
    return room
