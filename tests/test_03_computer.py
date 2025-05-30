#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: test_computer.py
#################################################################

import pytest
from room_project.room_logic.computer import ComputerRoom
import os
from pathlib import Path


# Test of the creation of a valid computer room
def test_create_valid_computer_room():
    room = ComputerRoom("ComputerTestRoom", capacity=6)
    assert room.name == "ComputerTestRoom"
    assert room.capacity == 6
    assert room.return_type() == "Computer Room"
    assert room.equipment == ["computer", "projector", "whiteboard"]

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of __str__ and __repr__ methods
def test_str_and_repr():
    room = ComputerRoom("ComputerTestRoom", capacity=6)
    assert (
        str(room)
        == "Computer Room: ComputerTestRoom, Capacity: 6, Equipment: computer, projector, whiteboard"
    )
    assert (
        repr(room)
        == "ComputerRoom(name=ComputerTestRoom, capacity=6, equipment=['computer', 'projector', 'whiteboard'])"
    )

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of return_equipment method
def test_return_equipment():
    room = ComputerRoom("ComputerTestRoom", capacity=6)
    assert room.return_equipment() == "Equipment: computer, projector, whiteboard"

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of return_type method
def test_return_type():
    room = ComputerRoom("ComputerTestRoom", capacity=6)
    assert room.return_type() == "Computer Room"

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of adding and removing a reservation
def test_add_and_remove_reservation():
    room = ComputerRoom("ComputerTestRoom2", capacity=6)
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
    room = ComputerRoom("ComputerTestRoom", capacity=6)

    # Test of adding an invalid reservation
    with pytest.raises(ValueError):
        room.add_reservation({"14/05/2025": [10, 0]})

    # Test of removing an invalid reservation
    assert not room.remove_reservation({"14/05/2025": [10, 0]})

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of too_small method
def test_too_small():
    room = ComputerRoom("ComputerTestRoom", capacity=6)
    assert not room.too_small(5)
    assert not room.too_small(6)
    assert room.too_small(7)

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test of reservation_duration_valid method
def test_reservation_duration_valid():
    room = ComputerRoom("ComputerTestRoom", capacity=6)
    assert not room.reservation_duration_valid(29)
    assert room.reservation_duration_valid(30)
    assert room.reservation_duration_valid(60)

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)
