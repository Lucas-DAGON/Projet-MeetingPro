#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: conference.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: Class for managing conference rooms.
#################################################################

# Import necessary modules
from .standard import Standard


class Conference(Standard):
    def __init__(self, name: str, capacity: int = 10):
        """
        Initialize a conference meeting room.

        :param name: Name of the meeting room.
        :param capacity: Maximum capacity of the meeting room.
        """
        super().__init__(
            name, capacity, {}
        )  # Add {} because of some tests which showed can retain older reservations -- Don't know why
        self.name = name
        self.capacity = capacity

    def __str__(self):
        """
        Return a string representation of the conference meeting room.

        :return: String representation of the conference meeting room.
        """
        return f"Conference Room: {self.name}, Capacity: {self.capacity}"

    def __repr__(self):
        """
        Return a string representation of the conference meeting room for debugging.

        :return: String representation of the conference meeting room for debugging.
        """
        return f"Conference(name={self.name}, capacity={self.capacity})"

    def too_big(self, number_of_people: int) -> bool:
        """
        Check if the meeting room is too big for the given number of people.

        :param number_of_people: Number of people to accommodate.
        :return: True if the room is too big, False otherwise.
        """
        return number_of_people < 4

    def return_type(self):
        """
        Return the type of the meeting room.

        :return: Type of the meeting room.
        """
        return "Conference Room"
