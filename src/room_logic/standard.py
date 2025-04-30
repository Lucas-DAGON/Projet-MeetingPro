#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: standard.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: Class for managing standard meeting rooms.
#################################################################

# Import necessary modules
from typing import List


class Standard:
    def __init__(self,name:str, capacity:int = 4):
        """
        Initialize a standard meeting room.

        :param name: Name of the meeting room.
        :param capacity: Maximum capacity of the meeting room.
        """
        self.name = name
        self.capacity = capacity

    def __str__(self):
        """
        Return a string representation of the standard meeting room.

        :return: String representation of the standard meeting room.
        """
        return f"Standard Room: {self.name}, Capacity: {self.capacity}"
    
    def __repr__(self):
        """
        Return a string representation of the standard meeting room for debugging.

        :return: String representation of the standard meeting room for debugging.
        """
        return f"Standard(name={self.name}, capacity={self.capacity})"
    
    def too_small(self, number_of_people:int) -> bool:
        """
        Check if the meeting room is too small for the given number of people.

        :param number_of_people: Number of people to accommodate.
        :return: True if the room is too small, False otherwise.
        """
        return number_of_people > self.capacity
    
    def reservation_duration_valid(self, duration:int) -> bool:
        """
        Check if the reservation duration is valid.

        :param duration: Duration of the reservation in minutes.
        :return: True if the duration is valid, False otherwise.
        """
        return 30 <= duration

    def is_available(self, start_time: List[int], end_time: List[int]) -> bool:
        """
        Check if the meeting room is available for the given time.

        :param start_time: Start time of the reservation as [minute, hour, day, month, year].
        :param end_time: End time of the reservation as [minute, hour, day, month, year].
        :return: True if the room is available, False otherwise.
        """
        if len(start_time) != 5 or len(end_time) != 5:
            raise ValueError("Time format must be a list of 5 integers: [minute, hour, day, month, year]")

        # Placeholder logic for availability check
        return True

    def Avaible_starting_of(self) -> List[int]:
        """
        Get the available starting time for the meeting room.

        :return: List of integers representing the available starting time as [minute, hour, day, month, year].
        """
        # Placeholder logic for available starting time
        return [0, 9, 1, 1, 2025]
    
    def return_type(self) -> str:
        """
        Return the type of the meeting room.

        :return: String representing the type of the meeting room.
        """
        return "Standard"