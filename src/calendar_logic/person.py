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
from json import JSONDecodeError, dumps, loads
from typing import List
from os import path
from pathlib import Path
import logging
import hmac
import hashlib

# Todo:
# - Discuss if we should implement a secret key or leave it like this
SecretKey = "secret_key".encode('utf-8')

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Define the Person class
class Person:
    def __init__(self, firstname: str, sirname: str, email: str):
        self.firstname = firstname
        self.sirname = sirname
        self.name = f"{self.firstname} {self.sirname}"
        self.email = email
        # Check for void_person
        if self.name == " " and self.email == "":
            # If we have a we will give it a "" id to avoid errors by printing
            self.id = ""
            # We will not save the person to a file
            logger.debug("Creating a void person")
            return
        # Check if the email is valid
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email address")
        self.reservations = []
        self.id = None
        # Generate a unique id for the person
        self.id_generator()
        # Ensure the id is unique
        if self.id is None:
            raise ValueError("ID generation failed")
        logger.debug(f"Name: {self.name}, Email: {self.email}, ID: {self.id}")
        # save the person in a json file named after the id
        # the file is stored in the relative path ../../persons/
        self.file_path = path.join(Path(__file__).parent.parent.parent, 'persons', f'{self.id}.json')
        # Check if the file already exists
        if path.exists(self.file_path):
            # If it's the case, it means the person already exists
            # We will therefore raise an error
            raise ValueError("This person already exists.")
        self.save_to_file()

    def add_reservation(self, reservation_data: List):
        if len(reservation_data) != 11:
            raise ValueError("La réservation doit contenir exactement 11 éléments")

        reservation = {
            "room_name": reservation_data[0],
            "start": {
                "minute": reservation_data[1],
                "hour": reservation_data[2],
                "day": reservation_data[3],
                "month": reservation_data[4],
                "year": reservation_data[5]
            },
            "end": {
                "minute": reservation_data[6],
                "hour": reservation_data[7],
                "day": reservation_data[8],
                "month": reservation_data[9],
                "year": reservation_data[10]
            }
        }

        if reservation in self.reservations:
            raise ValueError("Cette réservation existe déjà.")

        self.reservations.append(reservation)
        logger.debug("Réservations après ajout : %s", self.reservations)
        self.save_to_file()

    def remove_reservation(self, reservation_data: List):
        if len(reservation_data) != 11:
            raise ValueError("La réservation doit contenir exactement 11 éléments")

        target_reservation = {
            "room_name": reservation_data[0],
            "start": {
                "minute": reservation_data[1],
                "hour": reservation_data[2],
                "day": reservation_data[3],
                "month": reservation_data[4],
                "year": reservation_data[5]
            },
            "end": {
                "minute": reservation_data[6],
                "hour": reservation_data[7],
                "day": reservation_data[8],
                "month": reservation_data[9],
                "year": reservation_data[10]
            }
        }

        # Comparaison manuelle
        for existing in self.reservations:
            if existing == target_reservation:
                self.reservations.remove(existing)
                self.save_to_file()
                return

        raise ValueError("Réservation non trouvée")

    def get_reservations(self):
        return self.reservations
    
    def id_generator(self):
        """ 
        Generate a unique id for the person
        The name and email are used to generate a unique id
        """
        if self.name is None or self.email is None:
            raise ValueError("Name and email must be set before generating an id")
        if self.name == "" or self.email == "":
            raise ValueError("Name and email must not be empty")
        if self.id is not None:
            raise ValueError("ID already generated")
        else:
            # The idea is to use the name and email to generate the id and to find the person,
            # but at the same time not be able with the id alone to find the person
            data = f"{self.name}{self.email}".encode('utf-8')
            # Generate a hash of the data using HMAC and SHA256
            h = hmac.new(SecretKey, data, hashlib.sha256)
            # Convert the hash to a hexadecimal string
            self.id = h.hexdigest()
        return
    
    def __str__(self):
        return f"Person(name={self.name}, email={self.email}, id={self.id})"
    
    def __repr__(self):
        return f"Person(name={self.name}, email={self.email}, id={self.id})"
    
    def save_to_file(self):
        data = {
            "firstname": self.firstname,
            "sirname": self.sirname,
            "name": self.name,
            "email": self.email,
            "reservations": self.reservations,
            "id": self.id
        }
        logger.debug(f"Saving person data to {Path(self.file_path)}")
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
        # close the file
        logger.debug(f"Person data saved to {Path(self.file_path)}")
        f.close()

    # Alternative constructor for creating a person from a json file
    @classmethod
    def from_json(cls, json_data):
        try:
            logging.debug(f"Loading person data from json: {json_data}")
            # Load the json data
            # We will use the dumps method to convert the json data to a string
            data = loads(json_data)
            firstname = data.get('firstname')
            sirname = data.get('sirname')
            email = data.get('email')
            person = cls(firstname, sirname, email)
            person.reservations = data.get('reservations', [])
            person.id = data.get('id')
            return person
        except JSONDecodeError:
            raise ValueError("Invalid JSON data")

    # Alternative constructor for void person (unknown person)
    @classmethod
    def void_person(cls):
        # Create a void person with empty name and email
        # This person will not be saved to a file
        return cls("", "", "")

    # Alternative constructor for creating a person from a search for a person
    @classmethod
    def from_search(cls, ID: str):
        # Check if the file exists
        file_path = path.join(Path(__file__).parent.parent.parent, 'persons', f'{ID}.json')
        if not path.exists(file_path):
            # If the file does not exist, we will return a void person
            logger.debug(f"File {file_path} does not exist")
            return cls.void_person()
        # Read the file
        with open(file_path, 'r') as f:
            data = f.read()
        # Create a person from the json data
        logger.debug(f"json data: {data}")
        # We will use the from_json method to create the person
        return cls.from_json(data)


if __name__ == "__main__":
    # Example usage
    person = Person("John", "Doe", "jone_doe@uha.fr")
    print("\n\n",person,"\n\n")
    ID = person.id
    del person
    # Test the void person
    void_person = Person.void_person()
    print("\n\n",void_person,"\n\n")
    # Test the from_search method
    person = Person.from_search(ID)
    print("\n\n",person,"\n\n")
    # Test the adding reservation


    # Création d'un utilisateur
    person = Person("Alice", "Durand", "alice_durand@uha.fr")
    print("Créé:", person)

    # Données de réservation
    reservation1 = ["Salle A", 0, 9, 10, 5, 2025, 0, 10, 10, 5, 2025]
    reservation2 = ["Salle B", 30, 14, 12, 5, 2025, 0, 15, 12, 5, 2025]
    
    # Ajout des réservations
    print("\nAjout de la première réservation...")
    person.add_reservation(reservation1)
    print("Réservations après ajout:", person.get_reservations())
    
    print("\nAjout de la deuxième réservation...")
    person.add_reservation(reservation2)
    print("Réservations après ajout:", person.get_reservations())

    print('reservation : ', person.reservations)

    # Suppression d'une réservation
    print("\nSuppression de la première réservation...")
    person.remove_reservation(reservation1)
    print("Réservations après suppression:", person.get_reservations())

    # Tentative de suppression d'une réservation inexistante
    print("\nSuppression d'une réservation non existante (devrait lever une erreur)...")
    try:
        person.remove_reservation(reservation1)  # déjà supprimée
    except ValueError as e:
        print("Erreur attendue :", e)

    # Nettoyage (optionnel)
    print("\nTest terminé pour :", person.name)
