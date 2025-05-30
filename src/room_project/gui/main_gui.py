###########################################################################################
# -*- coding: utf-8 -*-
###########################################################################################
# Project: MeetingPro
# File: main_gui.py
###########################################################################################
# Creation Date: 23-04-2025
# Authors: Lucas DAGON
# Description: This script creates the main window.
###########################################################################################

import tkinter as tk

from tkinter import ttk, messagebox
from .bg_image import background_image
from .add_client_gui import add_client_gui
from ..controller.add_room import add_room
from ..controller.reservation import reserve_room
from ..controller.list_client import list_clients


class Main_Window:
    """Creates the main window of the application."""

    clients: list = []
    rooms: dict = {}
    reservations: dict = {}
    fullscreenstate: bool = False
    room_types: list = [
        "Standard",
        "Standard",
        "Conference Room",
        "Computer Room",
    ]  # "Standard" needs to be initialised twice so it is displayed correctly in the dropdown menu
    client_id: int = 0
    rooms_id: int = 0

    def __init__(self, master):
        self.master = master
        self.clients = list_clients()  # Load clients from the database
        self.client_id = len(self.clients)

        self.window = ttk.Notebook(master)
        self.window.pack(pady=10, expand=True, fill="both")

        self.frame_main = ttk.Frame(self.window)
        self.window.add(self.frame_main, text="Accueil")

        self.frame_add_client = ttk.Frame(self.window)
        self.window.add(self.frame_add_client, text="Ajouter")

        self.frame_reservation = ttk.Frame(self.window)
        self.window.add(self.frame_reservation, text="Réserver")

        self.frame_show_reservation = ttk.Frame(self.window)
        self.window.add(self.frame_show_reservation, text="Afficher")

        # Add "Ajouter" tab
        self.tab_add_client = ttk.Notebook(self.frame_add_client)
        self.tab_add_client.pack(expand=True, fill="both")

        self.tab_add_client.add(
            self.add_client_ui(self.tab_add_client), text="Ajouter un client"
        )
        self.tab_add_client.add(
            self.add_room_ui(self.tab_add_client), text="Ajouter une salle"
        )

        # Add "Réserver" tab
        self.tab_reservation = ttk.Notebook(self.frame_reservation)
        self.tab_reservation.pack(expand=True, fill="both")

        self.tab_reservation.add(
            self.reservation_room_ui(self.tab_reservation), text="Réserver une salle"
        )

        # Add "Afficher" tab
        self.tab_show = ttk.Notebook(self.frame_show_reservation)
        self.tab_show.pack(expand=True, fill="both")

        self.tab_show.add(self.show_room_ui(self.tab_show), text="Afficher les salles")
        self.tab_show.add(
            self.show_client_ui(self.tab_show), text="Afficher les clients"
        )
        self.tab_show.add(
            self.is_room_reservable_ui(self.tab_show),
            text="Afficher les salles disponibles",
        )

    #    def add_client(self, surname, name, email_address):
    #        if not surname or not name or not email_address:
    #            return "Erreur: Tous les champs doivent être remplis."
    #
    #        self.client_id = len(self.clients) + 1
    #        self.clients[self.client_id] = add_client(name, surname, email_address)
    #        return True

    def add_room(self, name_room, room_capacity, room_type):
        if not name_room:
            return "Erreur: Le nom de la salle doit être renseigné."

        self.rooms_id = len(self.rooms) + 1
        self.rooms[self.rooms_id] = add_room(name_room, room_capacity, room_type)
        return True

    def reserve_room(self, client_id, room_id, date_begin, date_end):
        if client_id not in self.clients:
            return "Erreur: Client non trouvé."
        if room_id not in self.rooms:
            return "Erreur: Salle non trouvée."
        if not self.rooms[room_id]["Disponible"]:
            return "Erreur: Salle non disponible."

        # room_reserved = reserve_room(, , room_id, client_id)
        return True

    def show_reservable_rooms(self, date_begin, date_end):
        self.room_reservable = [
            self.room for self.room in self.rooms if self.room["Disponible"]
        ]
        return self.room_reservable

    def add_client_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        ttk.Label(self.frame, text="Nom:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_surname = ttk.Entry(self.frame)
        self.entry_surname.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Prénom:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_name = ttk.Entry(self.frame)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Adresse email:").grid(
            row=2, column=0, padx=10, pady=10
        )
        self.entry_email = ttk.Entry(self.frame)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10)

        def validate():
            surname = self.entry_surname.get()
            name = self.entry_name.get()
            email = self.entry_email.get()
            (result, self.client_id, self.clients) = add_client_gui(
                surname, name, email, self.client_id, self.clients
            )
            if result is True:
                messagebox.showinfo("Succès", "Client ajouté avec succès!")
            else:
                messagebox.showerror("Erreur", result)

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        return self.frame

    def add_room_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        ttk.Label(self.frame, text="Nom de la salle:").grid(
            row=0, column=0, padx=10, pady=10
        )
        self.entry_room_name = ttk.Entry(self.frame)
        self.entry_room_name.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Capacitée de la salle:").grid(
            row=1, column=0, padx=10, pady=10
        )
        self.entry_room_capacity = ttk.Entry(self.frame)
        self.entry_room_capacity.grid(row=1, column=1, padx=10, pady=10)

        # Create an OptionMenu for room type selection
        self.entry_room_type = tk.StringVar(window)
        self.entry_room_type.set(self.room_types[0])  # default value
        ttk.Label(self.frame, text="Type de la salle:").grid(
            row=2, column=0, padx=10, pady=10
        )
        self.drop_down_menu = ttk.OptionMenu(
            self.frame, self.entry_room_type, *self.room_types
        ).grid(row=2, column=1, padx=10, pady=10)

        def validate():
            room_name = self.entry_room_name.get()
            room_capacity = int(self.entry_room_capacity.get())
            room_type = self.entry_room_type.get()
            result = self.add_room(room_name, room_capacity, room_type)
            if result is True:
                messagebox.showinfo("Succès", "Salle ajoutée avec succès!")
            else:
                messagebox.showerror("Erreur", result)

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        return self.frame

    def reservation_room_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        # Create an OptionMenu for room type selection
        self.entry_client_id = tk.StringVar(window)
        if not self.clients:
            # If no clients are registered, set a default value
            self.entry_client_id.set("pas de client enregistré")  # default value
            ttk.Label(self.frame, text="Client id:").grid(
                row=0, column=0, padx=10, pady=10
            )
            self.drop_down_menu_clients = ttk.OptionMenu(
                self.frame, self.entry_client_id, "pas de client enregistrer"
            ).grid(row=0, column=1, padx=10, pady=10)
        else:
            # If clients are registered, populate the dropdown with client names
            (self.client_id, self.client_name, self.client_mail), *self.rest = (
                self.clients
            )
            # self.entry_client_id.set(self.clients("name")) # default value
            ttk.Label(self.frame, text="Client id:").grid(
                row=0, column=0, padx=10, pady=10
            )
            self.drop_down_menu_clients = ttk.OptionMenu(
                self.frame, self.entry_client_id, *self.client_name
            ).grid(row=0, column=1, padx=10, pady=10)

        # Create an OptionMenu for room type selection
        self.entry_room_id = tk.StringVar(window)
        # self.entry_room_id.set(self.rooms(0)) # default value
        ttk.Label(self.frame, text="salle id:").grid(row=1, column=0, padx=10, pady=10)
        self.drop_down_menu_rooms = ttk.OptionMenu(
            self.frame, self.entry_room_id, *self.rooms
        ).grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Date de début:").grid(
            row=2, column=0, padx=10, pady=10
        )
        self.entry_date_begin = ttk.Entry(self.frame)
        self.entry_date_begin.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Date de fin:").grid(
            row=3, column=0, padx=10, pady=10
        )
        self.entry_date_end = ttk.Entry(self.frame)
        self.entry_date_end.grid(row=3, column=1, padx=10, pady=10)

        def validate():
            client_id = int(self.entry_client_id.get())
            room_id = int(self.entry_room_id.get())
            date_begin = self.entry_date_begin.get()
            date_end = self.entry_date_end.get()
            result = self.reserve_room(client_id, room_id, date_begin, date_end)
            if result is True:
                messagebox.showinfo("Succès", "Salle réservée avec succès!")
            else:
                messagebox.showerror("Erreur", result)

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        return self.frame

    def show_room_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        self.room_list = self.rooms
        self.text = tk.Text(self.frame)
        self.text.insert(
            tk.END,
            "\n".join(
                [
                    f"ID: {self.id}, Nom: {self.room['Nom']}, Disponible: {self.room['Disponible']}"
                    for self.id, self.room in enumerate(self.room_list, start=1)
                ]
            ),
        )
        self.text.pack(padx=10, pady=10)

        return self.frame

    def show_client_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        self.clients_list = self.clients
        self.text = tk.Text(self.frame)
        self.text.insert(
            tk.END,
            "\n".join(
                [
                    f"ID: {self.client['id']}, Nom: {self.client['name']}"
                    for self.id, self.client in enumerate(self.clients, start=1)
                ]
            ),
        )
        self.text.pack(padx=10, pady=10)

        return self.frame

    def is_room_reservable_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        self.date_begin = "2025-10-01"
        self.date_fin = "2023-10-02"
        self.salles_disponibles = self.show_reservable_rooms(
            self.date_begin, self.date_fin
        )
        self.text = tk.Text(self.frame)
        self.text.insert(
            tk.END,
            "\n".join(
                [
                    f"ID: {self.id}, Nom: {self.room['Nom']}"
                    for self.id, self.room in enumerate(
                        self.salles_disponibles, start=1
                    )
                ]
            ),
        )
        self.text.pack(padx=10, pady=10)

        return self.frame


def main():
    root = tk.Tk()
    app = Main_Window(root)
    root.mainloop()


if __name__ == "__main__":
    main()
