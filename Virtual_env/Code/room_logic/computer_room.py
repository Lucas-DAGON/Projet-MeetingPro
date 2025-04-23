#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: computer_room.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: Class for managing computer meeting rooms.
#################################################################

# Import necessary modules
from conference import Conference

class ComputerRoom(Conference):
    def __init__(self, name:str, capacity:int = 4):
        """
        Initialize a computer meeting room.

        :param name: Name of the meeting room.
        :param capacity: Maximum capacity of the meeting room.
        """
        super().__init__(name, capacity)
        self.equipment = ["computer", "projector", "whiteboard"]

    def return_equipment(self) -> str:
        """
        Return the equipment available in the computer meeting room.

        :return: String representation of the equipment.
        """
        return f"Equipment: {', '.join(self.equipment)}"
    
    def __str__(self):
        """
        Return a string representation of the computer meeting room.

        :return: String representation of the computer meeting room.
        """
        return f"Computer Room: {self.name}, Capacity: {self.capacity}, Equipment: {', '.join(self.equipment)}"
    
    def __repr__(self):
        """
        Return a string representation of the computer meeting room for debugging.

        :return: String representation of the computer meeting room for debugging.
        """
        return f"ComputerRoom(name={self.name}, capacity={self.capacity}, equipment={self.equipment})"

    def return_type(self) -> str:
        """
        Return the type of the meeting room.

        :return: Type of the meeting room.
        """
        return "Computer Room"
