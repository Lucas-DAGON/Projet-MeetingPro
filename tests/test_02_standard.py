#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: test_standard.py
#################################################################

import pytest
from room_project.room_logic.standard import Standard
import os
from pathlib import Path


# Test creation of a valid room
def test_create_valid_room():
    room = Standard("TestRoom", capacity=6)
    assert room.name == "TestRoom"
    assert room.capacity == 6
    assert room.return_type() == "Standard"

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of __str__ and __repr__ methods
def test_str_and_repr():
    room = Standard("TestRoom", capacity=6)
    assert str(room) == "Standard Room: TestRoom, Capacity: 6"
    assert repr(room) == "Standard(name=TestRoom, capacity=6)"

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of the too_small method
def test_too_small():
    room = Standard("TestRoom", capacity=6)
    assert not room.too_small(5)
    assert not room.too_small(6)
    assert room.too_small(7)

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of the reservation_duration_valid method
def test_reservation_duration_valid():
    room = Standard("TestRoom", capacity=6)
    assert not room.reservation_duration_valid(29)
    assert room.reservation_duration_valid(30)
    assert room.reservation_duration_valid(60)

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of adding and removing a reservation
def test_add_and_remove_reservation():
    room = Standard("TestRoom", capacity=6)
    reservation = {"14/05/2025": [10, 0, 11, 0]}

    # Adding a reservation
    room.add_reservation(reservation)
    assert reservation["14/05/2025"] in room.get_reservations()["14/05/2025"]

    # Removing a reservation
    assert room.remove_reservation(reservation)
    assert room.get_reservations() == {}

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of exceptions in add_reservation and remove_reservation
def test_add_and_remove_reservation_exceptions():
    room = Standard("TestRoom", capacity=6)

    # Test adding an invalid reservation
    with pytest.raises(ValueError):
        room.add_reservation({"14/05/2025": [10, 0]})

    # Test removing an invalid reservation
    assert not room.remove_reservation({"14/05/2025": [10, 0]})

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of save_to_file method
def test_save_to_file():
    room = Standard("TestRoom", capacity=6)
    assert os.path.exists(room.file_path)

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of load_from_json method
def test_load_from_json():
    # Create a room and save it
    room = Standard("TestRoom", capacity=6)
    room.add_reservation({"14/05/2025": [10, 0, 11, 0]})

    # Load the room from the JSON file
    loaded_room = Standard.load_from_json("TestRoom")
    assert loaded_room.name == "TestRoom"
    assert loaded_room.capacity == 6
    assert loaded_room.get_reservations() == {"14/05/2025": [[10, 0, 11, 0]]}

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of repeated removal of the same reservation
def test_repeated_remove_reservation():
    room = Standard("TestRoom", capacity=6)
    reservation = {"14/05/2025": [9, 0, 9, 30]}

    room.add_reservation(reservation)
    assert room.remove_reservation(reservation)
    assert not room.remove_reservation(reservation)

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test error when loading a non-existent room
def test_load_non_existent_room():
    with pytest.raises(FileNotFoundError):
        Standard.load_from_json("NonExistentRoom")
