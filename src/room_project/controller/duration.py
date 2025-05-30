#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: duration.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: A simple function to return the duration of a meeting
#################################################################

from datetime import datetime


def get_duration(bloc: list) -> str:
    """
    Returns the duration of a meeting in a human-readable format.

    :param bloc: A list in the format [hour_start_time, minute_start_time, hour_end_time, minute_end_time]
    :return: Duration as a string in the format "HH:MM".
    """
    # Verify the number of elements in the input list
    if len(bloc) != 4:
        raise ValueError(
            "Input list must contain exactly four elements: [hour_start_time, minute_start_time, hour_end_time, minute_end_time]"
        )

    # transform the list into a datetime object
    start_time = datetime(1, 1, 1, bloc[0], bloc[1])
    end_time = datetime(1, 1, 1, bloc[2], bloc[3])

    # Check if the end time is after the start time
    if end_time < start_time:
        raise ValueError("End time must be after start time.")

    # Calculate the duration
    duration = end_time - start_time
    hours, remainder = divmod(duration.total_seconds(), 3600)  # 3600 seconds in an hour
    minutes, _ = divmod(remainder, 60)  # 60 seconds in a minute

    # Format the duration as HH:MM
    return f"{int(hours):02}:{int(minutes):02}"


# Example usage:
if __name__ == "__main__":
    bloc = [9, 30, 11, 0]  # Example input
    try:
        duration = get_duration(bloc)
        print(f"Duration: {duration}")
    except ValueError as e:
        print(f"Error: {e}")
