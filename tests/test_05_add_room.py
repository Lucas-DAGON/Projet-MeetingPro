import pytest
from room_project.controller.add_room import add_room
from room_project.room_logic.standard import Standard
from room_project.room_logic.conference import Conference
from room_project.room_logic.computer import ComputerRoom
import os
from pathlib import Path


# Test adding a standard room
def test_add_standard_room():
    room = add_room("StandardRoom", 4, "Standard")
    assert isinstance(room, Standard)
    assert room.name == "StandardRoom"
    assert room.capacity == 4

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test adding a conference room
def test_add_conference_room():
    room = add_room("ConferenceRoom", 10, "Conference Room")
    assert isinstance(room, Conference)
    assert room.name == "ConferenceRoom"
    assert room.capacity == 10

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test adding a computer room
def test_add_computer_room():
    room = add_room("ComputerRoom", 6, "Computer Room")
    assert isinstance(room, ComputerRoom)
    assert room.name == "ComputerRoom"
    assert room.capacity == 6

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test adding a room with an invalid type
def test_add_room_invalid_type():
    with pytest.raises(ValueError):
        add_room("InvalidRoom", 4, "Invalid Type")
