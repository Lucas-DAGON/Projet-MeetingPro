#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: person.py
#################################################################
# Created Date: 2025-04-30
# Authors: GRIMM--KEMPF Matthieu
# Description: Person class for managing user information
#################################################################

# Import necessary modules
from json import loads, JSONDecodeError
from typing import List
from os import path
from pathlib import Path

# Define the Person class
class Person:
    def __init__(self, name: str, email: str):
        self.name = name
        self.email = email
        self.reservations = []
        self.id = None
        # Generate a unique id for the person
        self.id = self.id_generator()
        # Ensure the id is unique
        if self.id is None:
            raise ValueError("ID generation failed")
        # save the person in a json file named after the id
        # the file is stored in the relative path ../../persons/
        self.file_path = path.join(Path(__file__).parent.parent, 'persons', f'{self.id}.json')
        self.save_to_file()

    def add_reservation(self, reservation):
        self.reservations.append(reservation)
    
    def remove_reservation(self, reservation):
        if reservation in self.reservations:
            self.reservations.remove(reservation)
        else:
            raise ValueError("Reservation not found in user's reservations")
        
    def get_reservations(self):
        return self.reservations
    
    def id_generator(self):
        if self.id is None:
            self.id = hash((self.name, self.email))
        return self.id
    
    def __str__(self):
        return f"Person(name={self.name}, email={self.email}, id={self.id})"
    
    def __repr__(self):
        return f"Person(name={self.name}, email={self.email}, id={self.id})"
    
    def save_to_file(self):
        data = {
            "name": self.name,
            "email": self.email,
            "reservations": [res.__dict__ for res in self.reservations],
            "id": self.id
        }
        with open(self.file_path, 'w') as f:
            f.write(str(data))

    # Alternative constructor for creating a person from a json file
    @classmethod
    def from_json(cls, json_data):
        try:
            data = loads(json_data)
            name = data.get('name')
            email = data.get('email')
            return cls(name, email)
        except JSONDecodeError:
            raise ValueError("Invalid JSON data")
        

if __name__ == "__main__":
    # Example usage
    person = Person("John Doe", "jone_doe@uha.fr")
    print(person)