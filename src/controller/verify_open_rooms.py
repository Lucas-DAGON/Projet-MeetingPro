#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: verify_open_rooms.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: function to verify if each room is available
#              for the given time slot depending of its type
#              (meeting, conference, or computer room)
#################################################################

# Imports
import json
import os
from os import path
from pathlib import Path
from datetime import datetime
import logging

# Constants
ROOMS_DIR = path.join(Path(__file__).parent.parent.parent, "room")

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def check_overlap(start, end):
    """
    :param start: start time of the time slot in the format [hh:mm]
    :param end: end time of the time slot in the format [hh:mm]
    :return: start and end time in datetime format
    """
    logging.debug(f"Checking overlap between {start} and {end} in check_overlap")
    # Convert both list [h_start, m_start] and [h_end, m_end] in datetime logical format
    start_time = datetime.strptime(f"{start[0]:02}:{start[1]:02}", "%H:%M")
    end_time = datetime.strptime(f"{end[0]:02}:{end[1]:02}", "%H:%M")

    return start_time, end_time


def overlap(list1, list2):
    """
    :param list1: first time slot in the format [hh:mm, hh:mm]
    :param list2: second time slot in the format [hh:mm, hh:mm]
    :return: True if the two time slots overlap, False otherwise
    """
    logging.debug(f"Checking overlap between {list1} and {list2} in overlap")
    # Extract the start and end times from the lists
    start1, end1 = list1[:2], list1[2:]
    start2, end2 = list2[:2], list2[2:]

    # Convert the times to datetime objects
    start1, end1 = check_overlap(start1, end1)
    start2, end2 = check_overlap(start2, end2)

    # Vérify if the two time intervals overlap
    # Two intervals [start1, end1] and [start2, end2] overlap if:
    # max(start1, start2) < min(end1, end2)
    # This means that the start of one interval is before the end of the other interval
    # and the end of one interval is after the start of the other interval.
    # If the intervals overlap, return True
    return max(start1, start2) < min(end1, end2)


# fucntion to create a list of the rooms available for the given time slot
def verify_open_rooms(type: str, bloc: dict) -> list:
    """
    :param type: type of the room (Standard, Conference Room, Computer Room)
    :param bloc: dictionary containing a single entry where the single key is the day and
     its associated value is a list containing the start and end time of the time slot in
     the format [hh:mm, hh:mm]
    :return: list of the rooms available for the given time slot
    """
    # extracting the start and end time of the time slot
    # and the day of the week
    date, bloc = list(bloc.items())[0]
    logging.debug(f"Date: {date}, Bloc: {bloc}")
    free = []

    for file in os.listdir(ROOMS_DIR):
        logger.debug(f"Checking room file: {file}")
        # check if the file is a json file
        if file.endswith(".json"):
            route = os.path.join(ROOMS_DIR, file)
            with open(route, "r") as f:
                room = json.load(f)
                type_room = room.get("type", {})
                # check if the room is of the same type as the one requested
                if type_room != type:
                    continue
                # check if the room is available for the given time slot
                reservations = room.get("reservations", [])
                logging.debug(f"Reservations for {file}: {reservations}")
                # check if the room is available for the given time slot
                if date not in reservations:
                    free.append(file.replace(".json", ""))
                    logging.debug(f"Room {file} is free for {date}")
                else:
                    logging.debug(f"Reservations for {file} on {date}: {reservations}")
                    for res in reservations[date]:
                        logging.debug(f"Checking reservation: {res}")
                        if overlap(res, bloc[0]):
                            logging.debug(f"Room {file} is not free for {date}")
                            break
                    else:
                        free.append(file.replace(".json", ""))
                        logging.debug(
                            f"Room {file} is free for {date} after checking reservations"
                        )
    return free


# Example usage
if __name__ == "__main__":
    # Example of a bloc
    bloc = {
        "2025-04-23": [
            [
                9,
                0,  # Start time
                10,
                0,
            ],  # End time
        ]
    }
    # Example of a type
    type = "Standard"
    # Call the function
    available_rooms = verify_open_rooms(type, bloc)
    print(available_rooms)
