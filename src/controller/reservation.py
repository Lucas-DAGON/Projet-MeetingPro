#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: reservation.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: Functions for managing reservations of meeting rooms.
#################################################################

# Import necessary modules
from src.person_logic.person import Person
from src.room_logic.standard import Standard
from src.room_logic.conference import Conference
from src.room_logic.computer import ComputerRoom


def reserve_room(date, bloc, room: Standard, person: Person):
    """
    Function to reserve a room for a given time slot and person.
    :param room: Room object to be reserved
    :param start_time: Start time of the reservation in the format [hh:mm]
    :param end_time: End time of the reservation in the format [hh:mm]
    :param person: Person object making the reservation
    :return: None
    """
    # Create a reservation dictionary with the date and time slot for the person
    reservation_dict = {
        f"{date}": [bloc, room.name],
    }
    person.add_reservation(reservation_dict)
    # Create a reservation dictionary with the date and time slot for the room
    reservation_dict = {
        f"{date}": bloc,
    }
    room.add_reservation(reservation_dict)
    return True
