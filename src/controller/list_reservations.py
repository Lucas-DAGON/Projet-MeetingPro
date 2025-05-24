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
import src.person_logic.person as person


def list_reservations(person: person.Person):
    """
    Function to list all reservations of a person.
    :param person: Person object whose reservations are to be listed
    :return: List of reservations
    """
    # Get the list of reservations from the person object
    reservations = person.get_reservations()

    # Return the list of reservations
    return reservations
