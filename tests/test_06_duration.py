import pytest
from room_project.controller.duration import get_duration


# Test of the function get_duration with a valid input
def test_get_duration_valid_input():
    bloc = [9, 30, 11, 0]
    assert get_duration(bloc) == "01:30"


# Test of the function get_duration with a duration of less than one hour
def test_get_duration_less_than_one_hour():
    bloc = [9, 30, 10, 0]
    assert get_duration(bloc) == "00:30"


# Test of the function get_duration with a duration of more than one day
def test_get_duration_more_than_one_day():
    bloc = [9, 30, 33, 30]
    with pytest.raises(ValueError):
        get_duration(bloc)


# Test of the function get_duration with an invalid input (not enough elements)
def test_get_duration_invalid_input_length():
    bloc = [9, 30, 11]
    with pytest.raises(ValueError):
        get_duration(bloc)


# Test of the function get_duration with an invalid input (end time before start time)
def test_get_duration_invalid_end_time():
    bloc = [11, 0, 9, 30]
    with pytest.raises(ValueError):
        get_duration(bloc)


# Test of the function get_duration with an invalid input (invalid minutes)
def test_get_duration_invalid_minutes():
    bloc = [9, 70, 11, 0]
    with pytest.raises(ValueError):
        get_duration(bloc)


# Test of the function get_duration with an invalid input (invalid hours)
def test_get_duration_invalid_hours():
    bloc = [25, 0, 26, 0]
    with pytest.raises(ValueError):
        get_duration(bloc)
