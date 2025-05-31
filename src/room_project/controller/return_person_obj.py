#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: return_person_obj
#################################################################
# Created Date: 2025-05-31
# Authors: GRIMM--KEMPF Matthieu
# Description: Functions to return the object of a person.
#################################################################

# Import necessary module
from ..person_logic.person import Person


def return_person_obj(ID: str) -> Person:
    """
    A mock function to return a person object from an ID
    :param ID: The ID of the person
    """
    return Person.from_search(ID)
