import pytest
from room_project.person_logic.person import Person
import os
from pathlib import Path


# Test of the creation of a valid person
def test_create_valid_person():
    person = Person("Jean", "Dupont", "jean.dupont@example.com")
    assert person.name == "Jean Dupont"
    assert person.email == "jean.dupont@example.com"
    assert person.id is not None

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of the creation of a person with invalid email
def test_create_person_invalid_email():
    with pytest.raises(ValueError):
        Person("Alice", "Durand", "alice.durand[at]example.com")


# Test of creation of void person
def test_create_void_person():
    void_person = Person.void_person()
    assert void_person.name == " "
    assert void_person.email == ""
    assert void_person.id == ""


# Test add and remove reservation
def test_add_and_remove_reservation():
    person = Person("Marie", "Curie", "marie.curie@example.com")
    reservation = {"2025-05-15": [[14, 0, 15, 0], "Salle B"]}

    # Add a reservation
    person.add_reservation(reservation)
    assert reservation["2025-05-15"] == person.get_reservations()["2025-05-15"][0]

    # Remove a reservation
    person.remove_reservation(reservation)
    assert person.get_reservations() == {"2025-05-15": []}

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of overlapping reservation
def test_overlapping_reservation():
    person = Person("Isaac", "Newton", "isaac.newton@example.com")
    reservation1 = {"2025-06-03": [[9, 0, 10, 0], "Salle A"]}
    reservation2 = {"2025-06-03": [[9, 30, 10, 30], "Salle A"]}

    # Add a first reservation
    person.add_reservation(reservation1)

    # Attempt to add an overlapping reservation
    with pytest.raises(ValueError):
        person.add_reservation(reservation2)

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of removing a non-existent reservation
def test_remove_nonexistent_reservation():
    person = Person("Albert", "Einstein", "albert.einstein@example.com")
    reservation = {"2025-07-20": [[13, 0, 14, 0], "Salle B"]}

    # Attempt to remove a non-existent reservation
    with pytest.raises(ValueError):
        person.remove_reservation(reservation)

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of creating a person from a JSON file
def test_create_person_from_json():
    person = Person("Niels", "Bohr", "niels.bohr@example.com")
    with open(person.file_path, "r") as f:
        json_data = f.read()

    assert json_data is not None

    # Creating a person from the JSON data
    new_person = Person.from_save(json_data)
    assert new_person.name == "Niels Bohr"
    assert new_person.email == "niels.bohr@example.com"
    assert new_person.id == person.id

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of the id_generator method
def test_id_generator():
    person = Person("Jean", "Dupont", "jean.dupont@example.com")
    assert person.id is not None
    assert isinstance(person.id, str)

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of the save_to_file method
def test_save_to_file():
    person = Person("Jean", "Dupont", "jean.dupont@example.com")
    assert os.path.exists(person.file_path)

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of the __str__ and __repr__ methods
def test_str_and_repr():
    person = Person("Jean", "Dupont", "jean.dupont@example.com")
    assert (
        str(person)
        == f"Person(name=Jean Dupont, email=jean.dupont@example.com, id={person.id})"
    )
    assert (
        repr(person)
        == f"Person(name=Jean Dupont, email=jean.dupont@example.com, id={person.id})"
    )

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of exceptions in add_reservation and remove_reservation
def test_add_and_remove_reservation_exceptions():
    person = Person("Marie", "Curie", "marie.curie@example.com")

    # Test of adding an invalid reservation
    with pytest.raises(ValueError):
        person.add_reservation(
            {
                "2025-06-01": [[10, 0, 11, 0], "Salle C"],
                "2025-06-02": [[11, 0, 12, 0], "Salle D"],
            }
        )  # Invalid format

    # Test of removing an invalid reservation
    with pytest.raises(ValueError):
        person.remove_reservation({"2025-05-15": [[14, 0, 20, 10], "Salle B"]})

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test of the from_search method
def test_from_search():
    person = Person("Niels", "Bohr", "niels.bohr@example.com")
    person_id = person.id

    # Creating a person from a search ID
    new_person = Person.from_search(person_id)
    assert new_person.name == "Niels Bohr"
    assert new_person.email == "niels.bohr@example.com"
    assert new_person.id == person_id

    # Cleaning
    if person.file_path and os.path.exists(person.file_path):
        os.remove(person.file_path)


# Test multiple creation of the same person
def test_multiple_creation_same_person():
    person1 = Person("Marie", "Curie", "marie.curie@example.com")
    # Attempt to create the same person again
    with pytest.raises(ValueError):
        person2 = Person("Marie", "Curie", "marie.curie@example.com")

    # Clean up
    if person1.file_path and os.path.exists(person1.file_path):
        os.remove(person1.file_path)
