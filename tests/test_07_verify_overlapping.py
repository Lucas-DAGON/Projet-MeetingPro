import pytest
from datetime import datetime
from room_project.person_logic.verify_overlapping import (
    check_overlap,
    check_overlap_lists,
)


# Test of the check_overlap function
def test_check_overlap_returns_datetime_objects():
    start = [10, 30]
    end = [12, 0]
    result_start, result_end = check_overlap(start, end)
    assert isinstance(result_start, datetime)
    assert isinstance(result_end, datetime)
    assert result_start < result_end


@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        # Cases that overlap
        ([10, 0, 12, 0], [11, 0, 13, 0], True),
        ([9, 30, 11, 0], [10, 0, 10, 30], True),
        ([13, 0, 15, 0], [14, 0, 16, 0], True),
        ([8, 0, 10, 0], [9, 0, 11, 0], True),
        # Exactly equal cases
        ([9, 0, 11, 0], [9, 0, 11, 0], True),
        # Edge cases (no overlap)
        ([8, 0, 10, 0], [10, 0, 12, 0], False),
        ([13, 0, 14, 0], [14, 0, 15, 0], False),
        # Completely separate cases
        ([8, 0, 9, 0], [10, 0, 11, 0], False),
        ([15, 0, 16, 0], [13, 0, 14, 0], False),
        # Partial overlap (start before, end during)
        ([10, 0, 12, 0], [9, 0, 10, 30], True),
    ],
)
# Test of the check_overlap_lists function
def test_check_overlap_lists(list1, list2, expected):
    assert check_overlap_lists(list1, list2) == expected
