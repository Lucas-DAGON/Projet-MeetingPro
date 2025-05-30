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
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from src.gui.bg_image import background_image
from src.gui.add_client_gui import add_client_gui
from src.controller.add_room import add_room
from src.controller.reservation import reserve_room
from src.controller.list_client import list_clients
from src.controller.list_rooms import list_rooms
from src.controller.list_reservations import list_reservations






class Main_Window:
    """ Creates the main window of the application. """
    clients:dict = {}
    rooms:dict = {}
    reservations:dict = {}
    fullscreenstate:bool = False
    room_types:list = ["Standard", "Standard", "Conference Room", "Computer Room"] # "Standard" needs to be initialised twice so it is displayed correctly in the dropdown menu
    client_id:int = 0
    room_id:int = 0
    
    def __init__(self, master):
        self.master = master

        try:
            # Assuming that a list of clients, rooms and reservations already exists
            self.clients = list_clients()
            self.rooms = list_rooms()  
        except FileNotFoundError:
            pass  # If the file does not exist, we will start with empty lists

        self.client_id = len(self.clients)
        self.room_id = len(self.rooms)

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

        self.tab_add_client.add(self.add_client_ui(self.tab_add_client), text="Ajouter un client")
        self.tab_add_client.add(self.add_room_ui(self.tab_add_client), text="Ajouter une salle")
        


        # Add "Réserver" tab
        self.tab_reservation = ttk.Notebook(self.frame_reservation)
        self.tab_reservation.pack(expand=True, fill="both")

        self.tab_reservation.add(self.reservation_room_ui(self.tab_reservation), text="Réserver une salle")

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

    def reserve_room(self, client_id, room_id, date, Hour_of_meeting):
        if client_id not in self.clients:
            return "Erreur: Client non trouvé."
        if room_id not in self.rooms:
            return "Erreur: Salle non trouvée."
        if not self.rooms[room_id]["Disponible"]:
            return "Erreur: Salle non disponible."

        self.reservations = reserve_room(date, Hour_of_meeting, room_id, client_id)
        return True

    def show_reservable_rooms(self, date_begin, date_end):
        pass


    def add_client_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        ttk.Label(self.frame, text="Nom:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_surname = ttk.Entry(self.frame)
        self.entry_surname.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Prénom:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_name = ttk.Entry(self.frame)
        self.entry_name.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Adresse email:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_email = ttk.Entry(self.frame)
        self.entry_email.grid(row=2, column=1, padx=10, pady=10)

        def validate():
            surname = self.entry_surname.get()
            name = self.entry_name.get()
            email = self.entry_email.get()
            try: 
                (result, self.client_id, self.clients) = add_client_gui(surname, name, email, self.client_id, self.clients)
                if result is True:
                    messagebox.showinfo("Succès", "Client ajouté avec succès!")
                else:
                    messagebox.showerror("Erreur", result)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        return self.frame


    def add_room_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        ttk.Label(self.frame, text="Nom de la salle:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_room_name = ttk.Entry(self.frame)
        self.entry_room_name.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Capacitée de la salle:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_room_capacity = ttk.Entry(self.frame)
        self.entry_room_capacity.grid(row=1, column=1, padx=10, pady=10)

        # Create an OptionMenu for room type selection
        self.entry_room_type = tk.StringVar(window)
        self.entry_room_type.set(self.room_types[0]) # default value
        ttk.Label(self.frame, text="Type de la salle:").grid(row=2, column=0, padx=10, pady=10)
        self.drop_down_menu = ttk.OptionMenu(self.frame, self.entry_room_type, *self.room_types).grid(row=2, column=1, padx=10, pady=10)


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
        self.entry_room_id = tk.StringVar(window)
        if not self.clients:
            # If no clients are registered, set a default value
            self.entry_client_id.set("pas de client enregistré")  # default value that for some reason isn't displayed
            ttk.Label(self.frame, text="Client id:").grid(row=0, column=0, padx=10, pady=10)
            self.drop_down_menu_clients = ttk.OptionMenu(self.frame, self.entry_client_id, "pas de client enregistrer").grid(row=0, column=1, padx=10, pady=10)
        else:
            # If clients are registered, populate the dropdown with client names
            self.default =("choisie un nom")
            self.client_name = list(map(lambda x : x['name'], self.clients))
            self.entry_client_id.set(self.default) # default value that for some reason isn't displayed
            ttk.Label(self.frame, text="Client id:").grid(row=0, column=0, padx=10, pady=10)
            self.drop_down_menu_clients = ttk.OptionMenu(self.frame, self.entry_client_id, self.default, *self.client_name).grid(row=0, column=1, padx=10, pady=10)

        if not self.rooms:
            # If no clients are registered, set a default value
            self.entry_room_id.set("pas de salle enregistré")  # default value that for some reason isn't displayed
            ttk.Label(self.frame, text="Client id:").grid(row=0, column=0, padx=10, pady=10)
            self.drop_down_menu_rooms = ttk.OptionMenu(self.frame, self.entry_room_id, "pas de salle enregistré").grid(row=0, column=1, padx=10, pady=10)
        else:
            # Create an OptionMenu for room type selection
            self.default_room =("choisie une salles")
            self.room_name = list(map(lambda x : x['name'], self.rooms))
            self.entry_room_id.set(self.default_room) # default value that for some reason isn't displayed
            ttk.Label(self.frame, text="Salle id:").grid(row=1, column=0, padx=10, pady=10)
            self.drop_down_menu_rooms = ttk.OptionMenu(self.frame, self.entry_room_id, self.default_room, *self.room_name).grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Date:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_date = ttk.Entry(self.frame)
        self.entry_date.grid(row=2, column=1, padx=10, pady=10)

        # Beginning of the meeting
        ttk.Label(self.frame, text="heure de début:").grid(row=3, column=0, padx=10, pady=10)
        self.entry_hour_begin = ttk.Entry(self.frame)
        self.entry_hour_begin.grid(row=3, column=1, padx=10, pady=10)
        ttk.Label(self.frame, text="h").grid(row=3, column=2, padx=10, pady=10)

        self.entry_minute_begin = ttk.Entry(self.frame)
        self.entry_minute_begin.grid(row=3, column=3, padx=10, pady=10)
        ttk.Label(self.frame, text="min").grid(row=3, column=4, padx=10, pady=10)

        # End of the meeting
        ttk.Label(self.frame, text="heure de fin:").grid(row=4, column=0, padx=10, pady=10)
        self.entry_hour_end = ttk.Entry(self.frame)
        self.entry_hour_end.grid(row=4, column=1, padx=10, pady=10)
        ttk.Label(self.frame, text="h").grid(row=4, column=2, padx=10, pady=10)

        self.entry_minute_end = ttk.Entry(self.frame)
        self.entry_minute_end.grid(row=4, column=3, padx=10, pady=10)
        ttk.Label(self.frame, text="min").grid(row=4, column=4, padx=10, pady=10)

        def validate():
            client_name = self.entry_client_id.get()
            room_name = self.entry_room_id.get()
            date = self.entry_date.get()
            hours:list = []
            hours.append(self.entry_hour_begin.get())
            hours.append(self.entry_minute_begin.get())
            hours.append(self.entry_hour_end.get()) 
            hours.append(self.entry_minute_end.get()) 
            result = self.reserve_room(date, hours, room_name, client_name)
            if result is True:
                messagebox.showinfo("Succès", "Salle réservée avec succès!")
            else:
                messagebox.showerror("Erreur", result)

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

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
                    f"Nom: {self.room['name']}, Type: {self.room['type']}, Capacité: {self.room['capacity']}"
                    for self.id, self.room in enumerate(self.rooms, start=1)
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
                    f"Nom: {self.client['name']}, Email: {self.client['email']}"
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
        self.salles_disponibles = self.show_reservable_rooms(self.date_begin, self.date_fin)
        self.text = tk.Text(self.frame)
        self.text.insert(
            tk.END,
            "\n".join(
                [
                    f"Nom: {self.room['name']}, Type: {self.room['type']}, Capacité: {self.room['capacity']}"
                    for self.id, self.room in enumerate(self.rooms, start=1)
                ]
            ),
        )
        self.text.pack(padx=10, pady=10)

        return self.frame
   



def main(): 
    root = tk.Tk()
    app = Main_Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()