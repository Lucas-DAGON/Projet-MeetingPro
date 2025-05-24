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
from os import path
from pathlib import Path
import logging
import hmac
import hashlib
from verify_overlapping import check_overlap_lists

# Todo:
# - Discuss if we should implement a secret key or leave it like this
SecretKey = "secret_key".encode("utf-8")

# Set up logging
logging.basicConfig(level=logging.WARNING)
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
            # If we have a we will give it a "" id to avoid errors by printing
            self.id = ""
            # We will not save the person to a file
            logger.debug("Creating a void person")
            return
        # Check if the email is valid
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email address")
        # Create a void reservation dictionary it will contain our list of reservations
        self.reservations = {}
        self.id = None
        # Generate a unique id for the person
        self.id_generator()
        # Ensure the id is unique
        if self.id is None:
            raise ValueError("ID generation failed")
        logger.debug(f"Name: {self.name}, Email: {self.email}, ID: {self.id}")
        # save the person in a json file named after the id
        # the file is stored in the relative path ../../persons/
        self.file_path = path.join(
            Path(__file__).parent.parent.parent, "persons", f"{self.id}.json"
        )
        # Check if the file already exists
        if path.exists(self.file_path):
            # If it's the case, it means the person already exists
            # We will therefore raise an error
            raise ValueError("This person already exists or the id is not unique.")
        self.save_to_file()

    def add_reservation(self, reservation_data: dict):
        # The reservation_data should be a dictionary with a single entry and the key beeing the date "YYYY-MM-DD"
        # and the values being a list of lists containing the start and end time in the format [h_start,m_start,h_end,m_end]
        # and second element being the room name
        # example: {"2025-05-01": [[10, 0, 11, 0], "Salle A"]}

        if len(reservation_data) != 1:
            raise ValueError("Reservation data must contain exactly one entry")

        # Verify if the date (list(reservation_data.keys())[0]) is a key in the reservations
        if list(reservation_data.keys())[0] in self.reservations:
            # If the date is in reservation we will check if they overlap
            # the idea is if all reservations for this date overlap with the new reservation it
            # won't be possible to add it and we will raise an error
            for existing in self.reservations[list(reservation_data.keys())[0]]:
                # Cut the first element of the list to get the start and end time
                block = existing[0]
                # Check if the new reservation overlaps with the existing one
                if not check_overlap_lists(
                    block, reservation_data[list(reservation_data.keys())[0]][0]
                ):
                    self.reservations.append(reservation_data)
                    logger.debug("Réservation ajoutée : %s", reservation_data)
                    break
            else:
                # If we finish the loop without breaking, it means that the new reservation
                # overlaps with all existing reservations
                raise ValueError("La réservation chevauche une réservation existante")

        else:
            # If the date is not in the reservations, we will append it
            date = list(reservation_data.keys())[0]
            value = reservation_data[date]

            if date not in self.reservations:
                self.reservations[date] = []
            self.reservations[date].append(value)

        logger.debug("Réservations après ajout : %s", self.reservations)
        self.save_to_file()

    def remove_reservation(self, reservation_data: dict):
        # The reservation_data should be a dictionary with a single entry and the key beeing the date "YYYY-MM-DD"
        # and the values being a list of lists containing the start and end time in the format [h_start,m_start,h_end,m_end]
        # and second element being the room name
        # example: {"2025-05-01": [[10, 0, 11, 0], "Salle A"]}

        # Try to remove the entry (value) by using the key and the value
        try:
            self.reservations[list(reservation_data)[0]].remove(
                reservation_data[list(reservation_data)[0]]
            )
        except KeyError:
            # If the key does not exist, we will raise an error
            raise ValueError("La réservation n'existe pas")

        self.save_to_file()
        return

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
            data = f"{self.name}{self.email}".encode("utf-8")
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
            "id": self.id,
        }
        logger.debug(f"Saving person data to {Path(self.file_path)}")
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
        # close the file
        logger.debug(f"Person data saved to {Path(self.file_path)}")
        f.close()

    # Alternative constructor for creating a person from a json file
    @classmethod
    def from_save(cls, json_data):
        try:
            logging.debug(f"Loading person data from json: {json_data}")
            # Load the json data
            # We will use the dumps method to convert the json data to a string
            data = loads(json_data)
            firstname = data.get("firstname")
            sirname = data.get("sirname")
            email = data.get("email")
            person = cls(firstname, sirname, email)
            person.reservations = data.get("reservations", [])
            person.id = data.get("id")
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
        file_path = path.join(
            Path(__file__).parent.parent.parent, "persons", f"{ID}.json"
        )
        if not path.exists(file_path):
            # If the file does not exist, we will return a void person
            logger.debug(f"File {file_path} does not exist")
            return cls.void_person()
        # Read the file
        with open(file_path, "r") as f:
            data = f.read()
        # Create a person from the json data
        logger.debug(f"json data: {data}")
        # We will use the from_save method to create the person
        return cls.from_save(data)


if __name__ == "__main__":
    print("=== Début des tests rapides ===")
    import os
    import traceback

    # Test 1 : Création d'une personne valide
    try:
        p1 = Person("Jean", "Dupont", "jean.dupont@example.com")
        print("Test 1 : Création réussie ->", p1)
    except Exception as e:
        print("Test 1 : Échec de création -", e)
        traceback.print_exc()

    # Test 2 : Email invalide
    try:
        p2 = Person("Alice", "Durand", "alice.durand[at]example.com")
        print("Test 2 : Échec attendu non déclenché !")
    except ValueError as e:
        print("Test 2 : Erreur attendue ->", e)

    # Test 3 : Doublon de personne
    try:
        p3 = Person("Jean", "Dupont", "jean.dupont@example.com")
        print("Test 3 : Échec attendu non déclenché !")
    except ValueError as e:
        print("Test 3 : Erreur attendue ->", e)

    # Test 4 : Création d'une personne vide
    try:
        p4 = Person.void_person()
        print("Test 4 : Personne vide ->", p4)
    except Exception as e:
        print("Test 4 : Échec de création d'une personne vide -", e)
        traceback.print_exc()

    # Test 5 : Ajouter et supprimer une réservation
    try:
        p5 = Person("Marie", "Curie", "marie.curie@example.com")
        reservation = {"2025-05-15": [[14, 0, 15, 0], "Salle B"]}

        # Ajout
        p5.add_reservation(reservation)
        print("Test 5a : Réservation ajoutée ->", p5.get_reservations())

        # Suppression
        p5.remove_reservation(reservation)
        print("Test 5b : Réservation supprimée ->", p5.get_reservations())

        # Nettoyage
        if p5 and p5.file_path and os.path.exists(p5.file_path):
            os.remove(p5.file_path)
            print("Nettoyage : fichier de p5 supprimé")

    except Exception as e:
        print("Test 5 : Erreur pendant les réservations -", e)
        traceback.print_exc()

    # Test 6 : Déclencher toutes les erreurs de réservation
    try:
        p6 = Person("Isaac", "Newton", "isaac.newton@example.com")

        # Cas 1 : Mauvais format (plusieurs dates)
        try:
            p6.add_reservation(
                {
                    "2025-06-01": [[10, 0, 11, 0], "Salle C"],
                    "2025-06-02": [[11, 0, 12, 0], "Salle D"],
                }
            )
            print("Test 6a : ERREUR non détectée - Plusieurs dates")
        except ValueError as e:
            print("Test 6a : Erreur attendue (plusieurs dates) ->", e)

        # Cas 2 : Réservation normale
        valid_res = {"2025-06-03": [[9, 0, 10, 0], "Salle A"]}
        p6.add_reservation(valid_res)
        print("Test 6b : Réservation valide ajoutée")

        # Cas 3 : Réservation chevauchante
        conflict_res = {"2025-06-03": [[9, 30, 10, 30], "Salle A"]}
        try:
            p6.add_reservation(conflict_res)
            print("Test 6c : ERREUR non détectée - Réservation chevauchante")
        except ValueError as e:
            print("Test 6c : Erreur attendue (chevauchement) ->", e)

        # Cas 4 : Suppression d’une réservation inexistante
        fake_res = {"2025-06-04": [[13, 0, 14, 0], "Salle B"]}
        try:
            p6.remove_reservation(fake_res)
            print("Test 6d : ERREUR non détectée - Suppression impossible")
        except ValueError as e:
            print("Test 6d : Erreur attendue (suppression inexistante) ->", e)

        # Nettoyage
        if p6 and p6.file_path and os.path.exists(p6.file_path):
            os.remove(p6.file_path)
            print("Nettoyage : fichier de p6 supprimé")

    except Exception as e:
        print("Test 6 : Erreur inattendue -", e)
        traceback.print_exc()

    # Nettoyage : supprimer le fichier créé pour éviter des erreurs dans les tests suivants
    try:
        if p1 and p1.file_path and os.path.exists(p1.file_path):
            os.remove(p1.file_path)
            print("Nettoyage : fichier de p1 supprimé")
    except Exception as e:
        print("Erreur pendant le nettoyage :", e)

    print("=== Fin des tests rapides ===")
