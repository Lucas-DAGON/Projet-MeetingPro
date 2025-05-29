###########################################################################################
# -*- coding: utf-8 -*-
###########################################################################################
# Project: MeetingPro
# File: main_window.py
###########################################################################################
# Creation Date: 23-04-2025
# Authors: Lucas DAGON
# Description: This script creates the main window that can open all other windows.
###########################################################################################

import tkinter as tk
import os
import sys
from PIL import Image, ImageTk
from tkinter import ttk, messagebox
from src.controller.add_client import add_client
from src.controller.add_room import add_room






class Main_Window:
    """ Creates the main window of the application. """
    clients = {}
    rooms = {}
    reservations = {}
    fullscreenstate = False
    room_types = ["Standard", "Standard", "Conference Room", "Computer Room"] # "Standard" needs to be put initialised twice so it is display in dropdown menu
    
    def __init__(self, master):
        self.master = master
        

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

    def background_image(self, frame)-> None:
        """This function creates the background image of the gui."""
        # BG base path
        os.chdir(sys.path[0])

        # Change the path to the background image
        # Debugging
        if __name__ == "__main__":
            self.path_to_bg = "BG.jpg"
        else:
            self.path_to_bg = "src/gui/BG.jpg"

        self.full_path_to_bg:str = os.path.join(os.getcwd(), self.path_to_bg)
        self.image = Image.open(self.full_path_to_bg)
        self.image = ImageTk.PhotoImage(self.image, master = self.master)

        # Create a label to display the image
        self.image_label = tk.Label(frame, image = self.image)
        self.image_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.image_label.image = self.image

    def close_windows(self):
        self.master.destroy()

    def toggle_fullscreen(self, event=None):
        self.fullscreenstate = not self.fullscreenstate  # Just toggling the boolean
        self.master.attributes("-fullscreen", self.fullscreenstate)
        return "break"

    def end_fullscreen(self, event=None):
        self.fullscreenstate = False
        self.master.attributes("-fullscreen", False)
        return "break"
    
    def add_client(self, surname, name, email_address):
        if not surname or not name or not email_address:
            return "Erreur: Tous les champs doivent être remplis."

        self.client_id = len(self.clients) + 1
        self.clients[self.client_id] = add_client(name, surname, email_address)
        return True

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

        self.reservations[len(self.reservations) + 1] = {
            "Client ID": client_id,
            "Salle ID": room_id,
            "Date de début": date_begin,
            "Date de fin": date_end,
        }
        self.rooms[room_id]["Disponible"] = False
        return True


    def show_rooms(self):
        return list(self.rooms.values())


    def show_clients(self):
        return list(self.clients.values())


    def show_reservable_rooms(self, date_begin, date_end):
        self.room_reservable = [self.room for self.room in self.rooms.values() if self.room["Disponible"]]
        return self.room_reservable


    def add_client_ui(self, window):
        self.frame = ttk.Frame(window)
        self.background_image(self.frame)

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
            result = self.add_client(surname, name, email)
            if result is True:
                messagebox.showinfo("Succès", "Client ajouté avec succès!")
            else:
                messagebox.showerror("Erreur", result)

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        return self.frame


    def add_room_ui(self, window):
        self.frame = ttk.Frame(window)
        self.background_image(self.frame)

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
        self.background_image(self.frame)

        ttk.Label(self.frame, text="ID du client:").grid(row=0, column=0, padx=10, pady=10)
        self.entry_client_id = ttk.Entry(self.frame)
        self.entry_client_id.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="ID de la salle:").grid(row=1, column=0, padx=10, pady=10)
        self.entry_room_id = ttk.Entry(self.frame)
        self.entry_room_id.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Date de début:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_date_begin = ttk.Entry(self.frame)
        self.entry_date_begin.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(self.frame, text="Date de fin:").grid(row=3, column=0, padx=10, pady=10)
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
        self.background_image(self.frame)

        self.room_list = self.show_rooms()
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
        self.background_image(self.frame)

        self.clients_list = self.show_clients()
        self.text = tk.Text(self.frame)
        self.text.insert(
            tk.END,
            "\n".join(
                [
                    f"ID: {self.id}, Nom: {self.client['Nom']}, Prénom: {self.client['Prénom']}, Email: {self.client['Adresse email']}"
                    for self.id, self.client in enumerate(self.clients_list, start=1)
                ]
            ),
        )
        self.text.pack(padx=10, pady=10)

        return self.frame


    def is_room_reservable_ui(self, window):
        self.frame = ttk.Frame(window)
        self.background_image(self.frame)

        self.date_begin = "2025-10-01"  
        self.date_fin = "2023-10-02"
        self.salles_disponibles = self.show_reservable_rooms(self.date_begin, self.date_fin)
        self.text = tk.Text(self.frame)
        self.text.insert(
            tk.END,
            "\n".join(
                [
                    f"ID: {self.id}, Nom: {self.room['Nom']}"
                    for self.id, self.room in enumerate(self.salles_disponibles, start=1)
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