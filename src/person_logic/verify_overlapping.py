#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: verify overlapping.py
#################################################################
# Created Date: 2025-05-14
# Authors: GRIMM--KEMPF Matthieu
# Description: Fubnction to check if two time intervals overlap.
#################################################################


from datetime import datetime


def check_overlap(start, end):
    # Convert both list [h_start, m_start] and [h_end, m_end] in datetime logical format
    start_time = datetime.strptime(f"{start[0]:02}:{start[1]:02}", "%H:%M")
    end_time = datetime.strptime(f"{end[0]:02}:{end[1]:02}", "%H:%M")

    return start_time, end_time


def check_overlap_lists(list1, list2):
    # Extract the start and end times from the lists
    start1, end1 = list1[:2], list1[2:]
    start2, end2 = list2[:2], list2[2:]

    # Convert the times to datetime objects
    start1, end1 = check_overlap(start1, end1)
    start2, end2 = check_overlap(start2, end2)

    # Vérify if the two time intervals overlap
    # Two intervals [start1, end1] and [start2, end2] overlap if:
    # max(start1, start2) < min(end1, end2)
    # This means that the start of one interval is before the end of the other interval
    # and the end of one interval is after the start of the other interval.
    # If the intervals overlap, return True
    return max(start1, start2) < min(end1, end2)
