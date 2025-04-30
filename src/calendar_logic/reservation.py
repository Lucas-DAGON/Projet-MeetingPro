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
from datetime import datetime, timedelta
from json import loads, dumps, JSONDecodeError
from os import path
from typing import List
import room_logic as rl
from person import Person

def add_reservation(file_path : str, room : rl.Standard ,start_time : List[int], end_time : List[int], Reserver : Person, attendees : List[Person]) -> bool:
    if room.return_type() == "Standard":
        room = rl.Standard(room.name, room.capacity)
    elif room.return_type() == "Conference":
        room = rl.Conference(room.name, room.capacity)
    elif room.return_type() == "Computer Room":
        room = rl.ComputerRoom(room.name, room.capacity)
    else:
        raise ValueError("Invalid room type")
    
    # Check if the reservation is valid
    if not room.reservation_duration_valid(end_time[0] - start_time[0]):
        raise ValueError("Invalid reservation duration")
    if not room.is_available(start_time, end_time):
        raise ValueError("Room is not available for the selected time")
    if room.too_small(len(attendees)):
        raise ValueError("Room is too small for the number of attendees")
   
    
    # save the reservation in a json file

