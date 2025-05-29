#################################################################
# -*- coding: utf-8 -*-
#################################################################
# Project: MeetingPro
# File: list_client.py
#################################################################
# Created Date: 2025-04-23
# Authors: GRIMM--KEMPF Matthieu
# Description: Functions for listing clients
#################################################################

# Imports
from json import loads
from os import path, listdir
from pathlib import Path

# Constants
CLIENTS_DIR = path.join(Path(__file__).parent.parent.parent, "persons")


def list_clients():
    """
    Function to list all clients in the database
    :return: List of clients
    """
    clients = []
    for filename in listdir(CLIENTS_DIR):
        # open each file and load the full name and id
        with open(path.join(CLIENTS_DIR, filename), "r") as f:
            data = loads(f.read())
            client = {"id": data["id"], "name": data["name"]}
            clients.append(client)
    # Sort the list of clients by full name
    clients.sort(key=lambda x: x["name"])
    # Return the list of clients
    return clients
