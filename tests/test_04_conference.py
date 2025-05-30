import pytest
from room_project.room_logic.conference import Conference
import os
from pathlib import Path


# Test the creation of a valid conference room
def test_create_valid_conference_room():
    room = Conference("ConferenceTestRoom", capacity=10)
    assert room.name == "ConferenceTestRoom"
    assert room.capacity == 10
    assert room.return_type() == "Conference Room"

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test the __str__ and __repr__ methods
def test_str_and_repr():
    room = Conference("ConferenceTestRoom", capacity=10)
    assert str(room) == "Conference Room: ConferenceTestRoom, Capacity: 10"
    assert repr(room) == "Conference(name=ConferenceTestRoom, capacity=10)"

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test the too_big method
def test_too_big():
    room = Conference("ConferenceTestRoom", capacity=10)
    assert room.too_big(3)  # True, because 3 < 4
    assert not room.too_big(4)  # False, because 4 == 4
    assert not room.too_big(5)  # False, because 5 > 4

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test the return_type method
def test_return_type():
    room = Conference("ConferenceTestRoom", capacity=10)
    assert room.return_type() == "Conference Room"

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test adding and removing a reservation
def test_add_and_remove_reservation():
    room = Conference("ConferenceTestRoom", capacity=10)
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


# Test the exceptions in add_reservation and remove_reservation
def test_add_and_remove_reservation_exceptions():
    room = Conference("ConferenceTestRoom", capacity=10)

    # Test adding an invalid reservation
    with pytest.raises(ValueError):
        room.add_reservation({"14/05/2025": [10, 0]})

    # Test removing an invalid reservation
    assert not room.remove_reservation({"14/05/2025": [10, 0]})

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test the too_small method
def test_too_small():
    room = Conference("ConferenceTestRoom", capacity=10)
    assert not room.too_small(9)
    assert not room.too_small(10)
    assert room.too_small(11)

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)


# Test the reservation_duration_valid method
def test_reservation_duration_valid():
    room = Conference("ConferenceTestRoom", capacity=10)
    assert not room.reservation_duration_valid(29)
    assert room.reservation_duration_valid(30)
    assert room.reservation_duration_valid(60)

    # Cleanup
    if room.file_path and os.path.exists(room.file_path):
        os.remove(room.file_path)
