#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: list_reservations.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: Functions to list reservations of a person
#################################################################

# Imports
from ..person_logic import person


def list_reservations(person: person.Person):
    """
    Function to list all reservations of a person.
    :param person: Person object whose reservations are to be listed
    :return: List of reservations in dict form
    """
    # Get the list of reservations from the person object
    reservations = person.get_reservations()

    reservations_to_return = []  # changed by Matthieu

    for date in list(reservations.keys()):
        for info in reservations[date]:
            reservations_to_return.append(
                {"date": date, "time": info[0], "room": info[1]}
            )

    # Return the list of reservations
    return reservations_to_return
