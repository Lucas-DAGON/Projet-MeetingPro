#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: add_room.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: function to add a room to the database
#################################################################

# Imports
from ..room_logic.standard import Standard
from ..room_logic.conference import Conference
from ..room_logic.computer import ComputerRoom


def add_room(name, capacity, type):
    """
    Function to add a room to the database
    :param name: Name of the room
    :param capacity: Capacity of the room
    :param type: Type of the room (standard, conference or computer)
    :return: Room object
    """
    if type not in ["Standard", "Conference Room", "Computer Room"]:
        raise ValueError("Type must be standard, conference or computer")
    elif type == "Standard":
        room = Standard(name=name, capacity=capacity)
    elif type == "Conference Room":
        room = Conference(name=name, capacity=capacity)
    elif type == "Computer Room":
        room = ComputerRoom(name=name, capacity=capacity)
    else:
        raise ValueError(
            "Type must be standard, conference or computer"
        )  # This line is redundant due to the previous check, but kept for clarity.
    return room
