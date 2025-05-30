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
from ..person_logic.person import Person
from ..room_logic.standard import Standard
from ..room_logic.conference import Conference
from ..room_logic.computer import ComputerRoom


def reserve_room(date: str, bloc: list, room, person: Person) -> bool:
    """
    Function to reserve a room for a given time slot and person.
    :param date: Date of the reservation in 'YYYY/MM/DD' format
    :param bloc: Time slot for the reservation, e.g., [9,0, 10, 0] for 9:00 to 10:00
    :param room: Room object to be reserved (either Standard, Conference, or ComputerRoom)
    :param person: Person object making the reservation
    :return: True if ended properly
    """
    # Check if the duration of the bloc is valid
    if room.reservation_duration_valid(
        duration=(bloc[2] - bloc[0]) * 60 + (bloc[3] - bloc[1])
    ):
        raise ValueError("The duration of the reservation must be at least 30 minutes.")

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
