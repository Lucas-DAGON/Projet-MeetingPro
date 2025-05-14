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

    def is_available(self, start_time: List[int], end_time: List[int]) -> bool:
        """
        Check if the meeting room is available for the given time.

        :param start_time: Start time of the reservation as [minute, hour, day, month, year].
        :param end_time: End time of the reservation as [minute, hour, day, month, year].
        :return: True if the room is available, False otherwise.
        """
        if len(start_time) != 5 or len(end_time) != 5:
            raise ValueError("Time format must be a list of 5 integers: [minute, hour, day, month, year]")

        # Placeholder logic for availability check
        return True

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

    def return_type(self) -> str:
        """
        Return the type of the meeting room.

        :return: String representing the type of the meeting room.
        """
        return "Standard"
    
    def add_reservation(self, bloc : dict) -> None:
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
        self.reservations[date].sort(key=lambda x: (x[0], x[1]))  # Sort by start hour and minute
        self.save_to_json()
        logging.info(f"Reservation added for {self.name} on {bloc}: {self.reservations}")

    def remove_reservation(self, bloc : dict) -> bool:
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
            "reservations": self.reservations
        }
        # if the path and/or the file does not exist, we will create it
        if not path.exists(self.file_path):
            # create the directory if it does not exist
            Path(self.file_path).parent.mkdir(parents=True, exist_ok=True)
            # create the file
            with open(self.file_path, 'w') as f:
                f.write(dumps(data))
        else:
            # if the file exists, we will update it
            with open(self.file_path, 'r+') as f:
                f.seek(0)
                f.write(dumps(data))
                f.truncate()
        # close the file
        f.close()
        logging.info(f"Room {self.name} saved to {self.file_path}")
        return None

    @classmethod
    def load_from_json(cls, room_name: str) -> 'Standard':
        """
        Load a meeting room from a JSON file.

        :param room_name: Name of the meeting room.
        :return: Instance of the Standard class.
        """
        file_path = path.join(Path(__file__).parent.parent.parent, 'room', f'{room_name}.json')
        if not path.exists(file_path):
            raise FileNotFoundError(f"Room {room_name} not found.")
        
        with open(file_path, 'r') as f:
            room_data = load(f)  # Load the JSON data
            return cls(room_data['name'], room_data['capacity'], room_data['reservations'])


if __name__ == "__main__":
    # Example usage
    room = Standard("Conference Room", 10)
    print(room)
    print(room.is_available([0, 9, 1, 1, 2025], [30, 10, 1, 1, 2025]))
    logging.info("Room saved to JSON file.")
    del room
    room = Standard.load_from_json("Conference Room")
    logging.info("Room loaded from JSON file.")
    print(room)
    room.add_reservation({"12/05/2025": [9, 0, 10, 30]})
    print(room.get_reservations())
    room.add_reservation({"12/05/2025": [19, 0, 20, 30]})
    print(room.get_reservations())
    room.add_reservation({"13/05/2025": [19, 0, 20, 30]})
    print(room.get_reservations())
    print(room.Avaible_starting_of({"12/05/2025": [9, 0]}))
    print(room.Avaible_starting_of({"13/05/2025": [10, 0]}))
    room.add_reservation({"14/05/2025": [8, 0, 19, 0]})
    room.add_reservation({"14/05/2025": [19, 29, 20, 0]})
    print(room.Avaible_starting_of({"14/05/2025": [9, 0]}))