#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: standard.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: Class for managing standard meeting rooms.
#################################################################

# Import necessary modules
from typing import List
from json import dumps, load
from os import path
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Standard:
    def __init__(self,name:str, capacity:int = 4, reservations:dict = {}):
        """
        Initialize a standard meeting room.

        :param name: Name of the meeting room.
        :param capacity: Maximum capacity of the meeting room.
        """
        self.name = name
        self.capacity = capacity
        self.reservations = reservations  # Dictionary to hold reservations
        self.file_path = path.join(Path(__file__).parent.parent.parent, 'room', f'{self.name}.json') # Path to the JSON file for saving room data
        self.save_to_json() # Save the room to a JSON file upon initialization

    def __str__(self):
        """
        Return a string representation of the standard meeting room.

        :return: String representation of the standard meeting room.
        """
        return f"Standard Room: {self.name}, Capacity: {self.capacity}"
    
    def __repr__(self):
        """
        Return a string representation of the standard meeting room for debugging.

        :return: String representation of the standard meeting room for debugging.
        """
        return f"Standard(name={self.name}, capacity={self.capacity})"
    
    def too_small(self, number_of_people:int) -> bool:
        """
        Check if the meeting room is too small for the given number of people.

        :param number_of_people: Number of people to accommodate.
        :return: True if the room is too small, False otherwise.
        """
        return number_of_people > self.capacity
    
    def reservation_duration_valid(self, duration:int) -> bool:
        """
        Check if the reservation duration is valid.

        :param duration: Duration of the reservation in minutes.
        :return: True if the duration is valid, False otherwise.
        """
        return 30 <= duration

    def return_type(self) -> str:
        """
        Return the type of the meeting room.

        :return: String representing the type of the meeting room.
        """
        return "Standard"

    def add_reservation(self, bloc: dict) -> None:
        """
        Add a reservation for the meeting room.

        :param bloc: Dictionary containing reservation details. Keys are the date in format "dd/mm/yyyy" and values are a list with 4 entries: [start_hour, start_minute, end_hour, end_minute].
        :return: None
        """
        # extract the date and times from the bloc dictionary
        date = list(bloc.keys())[0]
        times = bloc[date]
        # add the reservation to the reservations dictionary
        if date not in self.reservations:
            self.reservations[date] = []
        self.reservations[date].append(times)
        # sort the reservations for that date (because we didn't change any other schedule)
        self.reservations[date].sort(
            key=lambda x: (x[0], x[1])
        )  # Sort by start hour and minute
        self.save_to_json()
        logging.info(
            f"Reservation added for {self.name} on {bloc}: {self.reservations}"
        )

    def remove_reservation(self, bloc: dict) -> bool:
        """
        Remove a reservation for the meeting room.

        :param bloc: Dictionary containing reservation details. Keys are the date in format "dd/mm/yyyy" and values are a list with 4 entries: [start_hour, start_minute, end_hour, end_minute].
        :return: True if the reservation was removed, False otherwise.
        """
        if bloc in self.reservations:
            self.reservations.remove(bloc)
            self.save_to_json()
            logging.info(f"Reservation removed for {self.name}: {bloc}")
            return True
        else:
            logging.warning(f"Reservation not found for {self.name}: {bloc}")
            return False

    def get_reservations(self) -> dict:
        """
        Get the reservations for the meeting room.

        :return: Dictionary of reservations with start time as key and end time as value.
        """
        return self.reservations

    def save_to_json(self) -> None:
        """
        Save the meeting room to a JSON file.

        :return: None
        """
        data = {
            "name": self.name,
            "type": self.return_type(),
            "capacity": self.capacity,
            "reservations": self.reservations,
        }
        # if the path and/or the file does not exist, we will create it
        if not path.exists(self.file_path):
            # create the directory if it does not exist
            Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
            # create the file
            with open(self.file_path, "w") as f:
                f.write(dumps(data))
        else:
            # if the file exists, we will update it
            with open(self.file_path, "r+") as f:
                f.seek(0)
                f.write(dumps(data))
                f.truncate()
        # close the file
        f.close()
        logging.info(f"Room {self.name} saved to {self.file_path}")
        return None

    @classmethod
    def load_from_json(cls, room_name: str) -> "Standard":
        """
        Load a meeting room from a JSON file.

        :param room_name: Name of the meeting room.
        :return: Instance of the Standard class.
        """
        file_path = path.join(
            Path(__file__).parent.parent.parent, "room", f"{room_name}.json"
        )
        if not path.exists(file_path):
            raise FileNotFoundError(f"Room {room_name} not found.")

        with open(file_path, "r") as f:
            room_data = load(f)  # Load the JSON data
            return cls(
                room_data["name"], room_data["capacity"], room_data["reservations"]
            )


if __name__ == "__main__":
    # Example usage
    room = Standard("Conference Room", 10)
    print(room)
    print("nothing")
    print(room.is_available([0, 9, 1, 1, 2025], [30, 10, 1, 1, 2025]))
    logging.info("Room saved to JSON file.")
    del room
    room = Standard.load_from_json("Conference Room")
    logging.info("Room loaded from JSON file.")
    print(room)
    for i in range(1000):