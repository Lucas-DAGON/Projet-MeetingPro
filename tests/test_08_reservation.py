import pytest
from room_project.controller.reservation import reserve_room
from room_project.person_logic.person import Person
from room_project.room_logic.standard import Standard
import os


# Test de la fonction reserve_room avec des entrées valides
def test_reserve_room_valid_input():
    # Créer une personne et une salle
    person = Person("Jean", "Dupont", "jean.dupont@example.com")
    room = Standard("TestRoom", capacity=6)

    # Réserver la salle
    date = "2025/05/15"
    bloc = [9, 0, 10, 30]
    assert reserve_room(date, bloc, room, person) is True

    # Vérifier que la réservation a été ajoutée à la personne et à la salle
    assert date in person.get_reservations()
    assert bloc in room.get_reservations()[date]

    # Nettoyage
    if (
        hasattr(person, "file_path")
        and person.file_path
        and os.path.exists(person.file_path)
    ):
        os.remove(person.file_path)
    if hasattr(room, "file_path") and room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test de la fonction reserve_room avec une durée de réservation invalide
def test_reserve_room_invalid_duration():
    # Créer une personne et une salle
    person = Person("Jean", "Dupont", "jean.dupont@example.com")
    room = Standard("TestRoom", capacity=6)

    # Essayer de réserver la salle avec une durée invalide
    date = "2025/05/15"
    bloc = [9, 0, 9, 15]  # Durée de 15 minutes, ce qui est invalide
    with pytest.raises(ValueError):
        reserve_room(date, bloc, room, person)

    # Nettoyage
    if (
        hasattr(person, "file_path")
        and person.file_path
        and os.path.exists(person.file_path)
    ):
        os.remove(person.file_path)
    if hasattr(room, "file_path") and room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test de la fonction reserve_room avec une heure de fin avant l'heure de début
def test_reserve_room_invalid_end_time():
    # Créer une personne et une salle
    person = Person("Jean", "Dupont", "jean.dupont@example.com")
    room = Standard("TestRoom", capacity=6)

    # Essayer de réserver la salle avec une heure de fin avant l'heure de début
    date = "2025/05/15"
    bloc = [10, 0, 9, 0]  # Heure de fin avant l'heure de début
    with pytest.raises(ValueError):
        reserve_room(date, bloc, room, person)

    # Nettoyage
    if (
        hasattr(person, "file_path")
        and person.file_path
        and os.path.exists(person.file_path)
    ):
        os.remove(person.file_path)
    if hasattr(room, "file_path") and room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)
