#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: standard.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: function to verify if each room is available
#              for the given time slot depending of its type
#              (meeting, conference, or computer room)
#################################################################

# Imports
import json

# fucntion to create a list of the rooms available for the given time slot
def verify_open_rooms(type : str, bloc :dict)-> list:
    """
    :param type: type of the room (meeting, conference, or computer room)
    :param bloc: dictionary containing a single entry where the single key is the day and
     its associated value is a list containing the start and end time of the time slot in
     the format [hh:mm, hh:mm]
    """
    # Load the list of rooms from the JSON file
    with open('src/room_logic/rooms.json', 'r') as f:
        rooms = json.load(f)

    # Create a list to store the available rooms
    available_rooms = []

    # Check if the room is available for the given time slot
    for room in rooms:

        if 
            # If its the right type we check if our start time is not already taken
            # by another meeting
            

    return available_rooms

    def Avaible_starting_of(self, current_time : dict) -> dict:
        """
        Get the available starting time for the meeting room.

        :param current_time: Dictionary containing one entry with the key in format "dd/mm/yyyy" and the value a liste in format [hour, minute].
        :return: dictionary with key as the date in format "dd/mm/yyyy" and value as a list in format [hour, minute].
        """
        if len(current_time) != 1:
            raise ValueError("Time format must be a dictionary with one entry: {date: [hour, minute]}")
        # Verify if the current_time key (the current day) is in the reservations
        if list(current_time.keys())[0] in self.reservations:
            # We initialize the current_end_time to the current_time
            current_end_time = current_time[list(current_time.keys())[0]]
            logging.debug(f"Current end time: {current_end_time}")
            # Take the first slot for the room after current time ([hour,minutes] in current_time) and the slot should be at least 30 minutes long
            for slot in self.reservations[list(current_time.keys())[0]]:
                logging.debug(f"Checking slot: {slot}")
                # Check if the slot is after the current time
                if (slot[0] > current_time[list(current_time.keys())[0]][0]) or ((slot[0] == current_time[list(current_time.keys())[0]][0]) and (slot[1] > current_time[list(current_time.keys())[0]][1])):
                    # Check if time between the current time and the slot is at least 30 minutes
                    if ((slot[0] - current_end_time[0]) * 60 + (slot[1] - current_end_time[1])) >= 30:
                        # If the slot is at least 30 minutes long, we will return the end time of the slot
                        return current_end_time
                    else:
                        # If the duration to the next slot is less than 30 minutes, we will refresh the current_end_time to the end time of the slot
                        current_end_time = [slot[2], slot[3]]
                        logging.debug(f"Current end time updated: {current_end_time}")
                # Verifies if the slot doesn't end after the current time
                elif (slot[2] > current_time[list(current_time.keys())[0]][0]) or ((slot[2] == current_time[list(current_time.keys())[0]][0]) and (slot[3] > current_time[list(current_time.keys())[0]][1])):
                    # If it's the case we will refresh the current_end_time to the end time of the slot
                    current_end_time = [slot[2], slot[3]]
                    logging.debug(f"Current end time updated: {current_end_time}")
            # If its the last slot of the day, we will return the end time of the last slot
            logging.debug(f"End of the last reservation of the day: {self.reservations[list(current_time.keys())[0]][-1][2]},{self.reservations[list(current_time.keys())[0]][-1][3]}") # print the last 2 elements of the last slot
            return [self.reservations[list(current_time.keys())[0]][-1][2], self.reservations[list(current_time.keys())[0]][-1][3]]
        # If the current_time key (the current day) is not in the reservations it means that the room is available all day
        # So we will return the current_time
        return current_time