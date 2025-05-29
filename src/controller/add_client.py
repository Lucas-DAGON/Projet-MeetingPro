#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: add_client.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: function to add a client to the database
#################################################################

# Imports
from src.person_logic.person import Person


def add_client(first_name:str, last_name:str, email:str) -> Person:
    """
    Function to add a client to the database
    :param first_name: First name of the client
    :param last_name: Last name of the client
    :param email: Email of the client
    :return: Person object
    """
    client = Person(first_name, last_name, email)
    return client
