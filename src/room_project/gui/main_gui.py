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

#Import necessary librairies
import tkinter as tk
from tkinter import ttk, messagebox
from .bg_image import background_image
from ..controller.add_room import add_room
from ..controller.reservation import reserve_room
from ..controller.list_client import list_clients
from ..controller.list_rooms import list_rooms
from ..controller.list_reservations import list_reservations
from ..controller.add_client import add_client
from ..controller.return_room_obj import return_room_object
from ..controller.return_person_obj import return_person_obj
from ..controller.duration import get_duration
from ..controller.verify_open_rooms import verify_open_rooms

###########################################################################################






class Main_Window:
    """ Creates the main window of the application. """
    clients:dict = {}
    rooms:dict = {}
    reservations:dict = {}
    room_types:list = ["Standard", "Conference Room", "Computer Room"]
    room_type:list = []
    room_name:list = []
    filtered_room_name = []
    filtered_client = {}
    filtered_room = {}
    room_capacity:list = []
    room_reservation:list = []
    hours = []

    
    def __init__(self, master):
        """ Initializes the main window and sets up the UI. """
        # Set the title of the main window
        master.title("MeetingPro")
        self.master = master

        try:
            # Assuming that a list of clients, rooms and reservations already exists
            self.clients = list_clients()
            self.rooms = list_rooms()  
        except FileNotFoundError:
            pass  # If the file does not exist, we will start with empty lists

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
        self.tab_show.add(self.show_client_ui(self.tab_show), text="Afficher les clients")
        self.tab_show.add(self.show_client_reservation_ui(self.tab_show),text="Afficher les réservations du clients")

        self.tab_show.add(self.show_if_room_reservable_ui(self.tab_show),text="Afficher les salles disponibles")

        # Add "Accueil" tab
        self.tab_main = ttk.Notebook(self.frame_main)
        self.tab_main.pack(expand=True, fill="both")

        self.tab_main.add(self.main_screen_ui(self.tab_main), text="Menu principal")


    def client_data_updater(self, text: tk.Text) -> None:
        """ Updates the data in the application. """
        text.config(state='normal')
        text.delete(1.0, tk.END)  # Clear the text widget before updating
        try:
            # Assuming that a list of clients already exists
            self.clients = list_clients() 
        except FileNotFoundError:
            text.insert(tk.END, "Aucun client enregistré.\n")
            text.config(state='disabled')
        
        self.clients = list_clients()
        temp_clients:dict = self.clients.copy()
        for item in temp_clients:
            item.pop('id', None)
        self.printTable(temp_clients, sep=' ', text = text)
        text.config(state='disabled')

    def room_data_updater(self, text: tk.Text) -> None:
        """ Updates the data in the application. """
        text.config(state='normal')
        text.delete(1.0, tk.END)  # Clear the text widget before updating
        try:
            # Assuming that a list of clients already exists
            self.rooms = list_rooms() 
        except FileNotFoundError:
            text.insert(tk.END, "Aucune salle enregistré.\n")
            text.config(state='disabled')

        self.printTable(self.rooms, sep=' ', text = text)
        text.config(state='disabled')
        
    def combobox_updater(self, combobox: ttk.Combobox, default:str, data:dict) -> None:
        """ Updates the dropdown menu with the list of clients. """
        data_values = list(map(lambda x : x['name'], data))
        combobox.config(values=data_values)
        combobox.set(default)

        
        



    def add_client(self, surname: str, name: str, email_address: str) -> bool:
        """ Adds a client to the application. """
        if not surname or not name or not email_address:
            return "Erreur: Tous les champs doivent être remplis."
        add_client(name, surname, email_address)
        return True

    def add_room(self, name_room, room_capacity, room_type):
        """ Adds a room to the application. """
        if not name_room:
            return "Erreur: Le nom de la salle doit être renseigné."

        add_room(name_room, room_capacity, room_type)
        return True

    def reserve_room(self, client_id, room_id, date, Hour_of_meeting):
        """ Reserves a room for a given date and time slot. """
        self.reservations = reserve_room(date, Hour_of_meeting, room_id, client_id)
        return True

    def get_meeting_time(self, hour:list) -> str:
        """ Returns the duration of a meeting in a human-readable format. """
        meeting_time = get_duration(hour)
        return meeting_time


    def main_screen_ui(self, window):
        """ Creates the main screen UI with buttons to navigate to other functionalities. """
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        self.button_add = ttk.Button(self.frame, text="Ajouter", command=self.go_to_add_client_ui)
        self.button_add.config(width=50, padding=10)
        self.button_add.grid(row=3, column=0, columnspan=2, padx=200, pady=50)

        self.button_add = ttk.Button(self.frame, text="Réservation", command=self.go_to_reservation_ui)
        self.button_add.config(width=50, padding=10)
        self.button_add.grid(row=5, column=0, columnspan=2, padx=200, pady=50)

        self.button_add = ttk.Button(self.frame, text="Afficher", command=self.go_to_show_ui)
        self.button_add.config(width=50, padding=10)
        self.button_add.grid(row=7, column=0, columnspan=2, padx=200, pady=50)

        return self.frame

    def go_to_reservation_ui(self):
        """ Switches to the 'Réserver' tab in the notebook. """
        self.window.select(self.frame_reservation)
        self.frame_reservation.tkraise()

    def go_to_add_client_ui(self):
        """ Switches to the 'Ajouter' tab in the notebook. """
        self.window.select(self.frame_add_client)
        self.frame_add_client.tkraise()

    def go_to_show_ui(self):
        """ Switches to the 'Afficher' tab in the notebook. """
        self.window.select(self.frame_show_reservation)
        self.frame_show_reservation.tkraise()

    def go_to_main_ui(self):
        """ Switches to the 'Accueil' tab in the notebook. """
        self.window.select(self.frame_main)
        self.frame_main.tkraise()

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
                result = self.add_client(surname, name, email)
                if result is True:
                # Update the client data
                 self.client_data_updater(self.text_client)
                 self.combobox_updater(self.combobox_clients, self.default_client, self.clients)
                 messagebox.showinfo("Succès", "Client ajouté avec succès!")
                 self.go_to_main_ui()
                else:
                    messagebox.showerror("Erreur", result)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=3, column=3, columnspan=2, padx=10, pady=10)

        self.button_cancel = ttk.Button(self.frame, text="Annuler", command=self.go_to_main_ui)
        self.button_cancel.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

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

        # Create an Combobox for room type selection
        ttk.Label(self.frame, text="Type de la salle:").grid(row=2, column=0, padx=10, pady=10)
        self.entry_room_type = ttk.Combobox(self.frame, values=self.room_types, state='readonly')
        self.entry_room_type.grid(row=2, column=1, padx=10, pady=10)
        self.entry_room_type.set("type de salle")  # Set a default value


        def validate():
            room_name = self.entry_room_name.get()
            room_capacity = int(self.entry_room_capacity.get())
            room_type = self.entry_room_type.get()
            try:
                result = self.add_room(room_name, room_capacity, room_type)
                if result is True:
                    # Update the room data
                    self.room_data_updater(self.text_room)
                    self.combobox_updater(self.combobox_rooms, self.default_room, self.rooms)
                    messagebox.showinfo("Succès", "Salle ajoutée avec succès!")
                    self.go_to_main_ui()
                else:
                    messagebox.showerror("Erreur", result)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=3, column=3, columnspan=2, padx=10, pady=10)

        self.button_cancel = ttk.Button(self.frame, text="Annuler", command=self.go_to_main_ui)
        self.button_cancel.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        return self.frame



    # Function for checking the
    # key pressed and updating
    # the listbox
    # Code adapted from the original snippet below:
    # https://www.geeksforgeeks.org/autocmplete-combobox-in-python-tkinter/
    def checkkey(self, event):
        """ Checks the key pressed and updates the combobox with the matching clients. """

        value = event.widget.get()

        # get data from l
        if not value:
            data = []
        else:
            data = []
            for item in self.client_name:
                if value.lower() in item.lower():
                    data.append(item)                
    
        # update data in listbox
        self.update(data)
    
    
    def update(self, data):
        """ Updates the combobox with the new data. """
        # if no data is found, set the default value
        if not data:
            self.client_name = list(map(lambda x : x['name'], self.clients))
            self.combobox_clients.config(values=self.client_name)
        else :
            # put new data
            self.combobox_clients.config(values=data)

    def checkkey_show(self, event):
        """ Checks the key pressed and updates the combobox with the matching clients. """

        value = event.widget.get()

        # get data from l
        if not value:
            data = []
        else:
            data = []
            for item in self.client_name:
                if value.lower() in item.lower():
                    data.append(item)                
    
        # update data in listbox
        self.update_show(data)
    
    
    def update_show(self, data):
        """ Updates the combobox with the new data. """
        # if no data is found, set the default value
        if not data:
            self.client_name = list(map(lambda x : x['name'], self.clients))
            self.combobox_clients_show.config(values=self.client_name)
        else :
            # put new data
            self.combobox_clients_show.config(values=data)


    def room_type_update(self):
        """ Updates the room combobox based on the selected room tupe. """
        self.filtered_room_name.clear()

        for name in [x for x in self.rooms if x['type'] == self.room_type_button.get()]:
            self.filtered_room_name.append(name)
        
        self.room_name = list(map(lambda x : x['name'], self.filtered_room_name))
        self.combobox_rooms.config(values=self.room_name)
        self.combobox_rooms.set(self.default_room)

        

    def reservation_room_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        # Create an Combobox for client selection
        ttk.Label(self.frame, text="Client:").grid(row=0, column=0, padx=10, pady=10)
        if not self.clients:
            # If no clients are registered, set a default value
            self.default_no_client:str = "pas de client enregistré"  # default value
            self.combobox_clients = ttk.Combobox(self.frame, values="", state='readonly')
            self.combobox_clients.grid(row=0, column=1, padx=10, pady=10)
            self.combobox_clients.set(self.default_no_client)
        else:
            # If clients are registered, populate the dropdown with client names
            self.client_name = list(map(lambda x : x['name'], self.clients))
            self.default_client:str = "Sélectionner un client"
            ttk.Label(self.frame, text="Client:").grid(row=0, column=0, padx=10, pady=10)
            self.combobox_clients = ttk.Combobox(self.frame)
            self.combobox_clients.grid(row=0, column=1, padx=10, pady=10)
            self.combobox_clients.bind("<KeyRelease>", self.checkkey)
            self.update(self.client_name)

        # Create an Combobox for room selection
        ttk.Label(self.frame, text="Salle:").grid(row=1, column=0, padx=10, pady=10)
        if not self.rooms:
            # If no clients are registered, set a default value
            self.default_no_room:str = "pas de salle enregistré"  # default value
            self.combobox_rooms = ttk.Combobox(self.frame, values="", state='readonly')
            self.combobox_rooms.grid(row=1, column=1, padx=10, pady=10)
            self.combobox_clients.set(self.default_no_room)
        else:
            self.default_room:str = "Sélectionner une salle"
            self.room_name = list(map(lambda x : x['name'], self.rooms))
            self.combobox_rooms = ttk.Combobox(self.frame, values=self.room_name, state='readonly')
            self.combobox_rooms.grid(row=1, column=1, padx=10, pady=10)
            self.combobox_rooms.set(self.default_room)

            self.room_type_button = tk.StringVar()
            self.radiobutton_standard = ttk.Radiobutton(self.frame, text="Standard", variable=self.room_type_button, value="Standard", command=self.room_type_update)
            self.radiobutton_standard.grid(row=1, column=2, padx=10, pady=10)
            self.radiobutton_standard.invoke()  # Set the default selection to "Standard"
            self.radiobutton_conference = ttk.Radiobutton(self.frame, text="Salle de conférence", variable=self.room_type_button, value="Conference Room", command=self.room_type_update)
            self.radiobutton_conference.grid(row=1, column=3, padx=10, pady=10)
            self.radiobutton_computer = ttk.Radiobutton(self.frame, text="Salle informatique", variable=self.room_type_button, value="Computer Room", command=self.room_type_update)
            self.radiobutton_computer.grid(row=1, column=4, padx=10, pady=10)

        # Date of the meeting
        ttk.Label(self.frame, text="Date:").grid(row=2, column=0, padx=10, pady=10)
        ttk.Label(self.frame, text="La date doit être au format jj-mm-aaaa").grid(row=2, column=2, padx=10, pady=10)
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
            # Put the selected client in a dictionary
            self.clients = list_clients()
            for name in [x for x in self.clients if x['name'] == self.combobox_clients.get()]:
                self.filtered_client.update(name)
            client_object = return_person_obj(self.filtered_client['id'])

            for name in [x for x in self.rooms if x['name'] == self.combobox_rooms.get()]:
                self.filtered_room.update(name)
            
            room_object = return_room_object(self.combobox_rooms.get(), self.room_type_button.get())

            date = self.entry_date.get()
            
            self.hours.clear()
            self.hours.append(int(self.entry_hour_begin.get()))
            self.hours.append(int(self.entry_minute_begin.get()))
            self.hours.append(int(self.entry_hour_end.get()))
            self.hours.append(int(self.entry_minute_end.get()))
            try:
                result = reserve_room(date, self.hours, room_object, client_object)
                if result is True:
                    messagebox.showinfo("Succès", "Salle réservée avec succès!")
                else:
                    messagebox.showerror("Erreur", result)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))

        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=5, column=3, columnspan=2, padx=10, pady=10)

        self.button_cancel = ttk.Button(self.frame, text="Annuler", command=self.go_to_main_ui)
        self.button_cancel.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        return self.frame

    def printTable(self, myDict, colList=None, sep='\uFFFA', text:tk.Text=None) -> str:
        """ Pretty print a list of dictionaries (myDict) as a dynamically sized table.
        If column names (colList) aren't specified, they will show in random order.
        sep: row separator. Ex: sep='\n' on Linux. Default: dummy to not split line.
        Author: Thierry Husson - Use it as you want but don't blame me.
        """
        if not colList: colList = list(myDict[0].keys() if myDict else [])
        myList = [colList] # 1st row = header
        for item in myDict: myList.append([str(item[col] or '') for col in colList])
        colSize = [max(map(len,(sep.join(col)).split(sep))) for col in zip(*myList)]
        formatStr = ' | '.join(["{{:<{}}}".format(i) for i in colSize])
        line = formatStr.replace(' | ','-+-').format(*['-' * i for i in colSize])
        item=myList.pop(0); lineDone=False
        while myList or any(item):
           if all(not i for i in item):
              item=myList.pop(0)
              if line and (sep!='\uFFFA' or not lineDone): text.insert(tk.END, line + '\n'); lineDone=True
           row = [i.split(sep,1) for i in item]
           text.insert(tk.END, formatStr.format(*[i[0] for i in row])+ '\n')
           item = [i[1] if len(i)>1 else '' for i in row]

    def show_room_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        self.text_room = tk.Text(self.frame)
        self.room_data_updater(self.text_room)
        self.text_room.pack(padx=10, pady=10)

        return self.frame


    def show_client_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        self.text_client = tk.Text(self.frame)
        # Insert the client data into the text widget
        self.client_data_updater(self.text_client)
        self.text_client.config(state='disabled')
        self.text_client.pack(padx=10, pady=10)

        return self.frame



    def show_client_reservation_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        self.text_client_reservation = tk.Text(self.frame, state='disabled')
        self.text_client_reservation.grid(row=0, column=2, padx=10, pady=10)
        self.combobox_clients_show = ttk.Combobox(self.frame)
        self.combobox_clients_show.grid(row=0, column=1, padx=10, pady=10)
        self.combobox_clients_show.bind("<KeyRelease>", self.checkkey_show)
        self.update_show(self.client_name)


        def validate():
            # Put the selected client in a dictionary
            try:
                self.clients = list_clients()
            except FileNotFoundError:
                self.text_client_reservation.config(state='normal')
                self.text_client_reservation.delete(1.0, tk.END)  # Clear the text widget before updating
                self.text_client_reservation.insert(tk.END, "Aucun client enregistré.\n")
                self.text_client_reservation.config(state='disabled')
                return


            for name in [x for x in self.clients if x['name'] == self.combobox_clients_show.get()]:
                self.filtered_client.update(name)
            client_object = return_person_obj(self.filtered_client['id'])


            try:
                # Get the reservations for the specified client
                result = list_reservations(client_object)
                if result is not None:
                    self.text_client_reservation.config(state='normal')
                    self.printTable(result, sep=' ', text=self.text_client_reservation)
                    self.text_client_reservation.config(state='disabled')
                else:
                    messagebox.showerror("Erreur", result)
            except ValueError as e:
                messagebox.showerror("Erreur", str(e))
                


        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=5, column=3, columnspan=2, padx=10, pady=10)

        self.button_cancel = ttk.Button(self.frame, text="Retour au menu principal", command=self.go_to_main_ui)
        self.button_cancel.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        return self.frame
   

    def show_if_room_reservable_ui(self, window):
        self.frame = ttk.Frame(window)
        background_image(self.frame)

        self.text_room_reservable = tk.Text(self.frame, state='disabled')
        self.text_room_reservable.grid(row=7, column=2, padx=10, pady=10)


        # Beginning Date of the meeting
        ttk.Label(self.frame, text="Date de début:").grid(row=2, column=0, padx=10, pady=10)
        ttk.Label(self.frame, text="La date doit être au format jj-mm-aaaa").grid(row=2, column=2, padx=10, pady=10)
        self.entry_date_begin = ttk.Entry(self.frame)
        self.entry_date_begin.grid(row=2, column=1, padx=10, pady=10)

        # Beginning time of the meeting
        ttk.Label(self.frame, text="heure de début:").grid(row=4, column=0, padx=10, pady=10)
        self.entry_hour_begin = ttk.Entry(self.frame)
        self.entry_hour_begin.grid(row=4, column=1, padx=10, pady=10)
        ttk.Label(self.frame, text="h").grid(row=4, column=2, padx=10, pady=10)

        self.entry_minute_begin = ttk.Entry(self.frame)
        self.entry_minute_begin.grid(row=4, column=3, padx=10, pady=10)
        ttk.Label(self.frame, text="min").grid(row=4, column=4, padx=10, pady=10)

        # End of the meeting
        ttk.Label(self.frame, text="heure de fin:").grid(row=5, column=0, padx=10, pady=10)
        self.entry_hour_end = ttk.Entry(self.frame)
        self.entry_hour_end.grid(row=5, column=1, padx=10, pady=10)
        ttk.Label(self.frame, text="h").grid(row=5, column=2, padx=10, pady=10)

        self.entry_minute_end = ttk.Entry(self.frame)
        self.entry_minute_end.grid(row=5, column=3, padx=10, pady=10)
        ttk.Label(self.frame, text="min").grid(row=5, column=4, padx=10, pady=10)

        # Type of room selection
        def validate():
            # Get the date and time inputs
            date_begin = self.entry_date_begin.get()
            self.hours.clear()
            self.hours.append(int(self.entry_hour_begin.get()))
            self.hours.append(int(self.entry_minute_begin.get()))
            self.hours.append(int(self.entry_hour_end.get()))
            self.hours.append(int(self.entry_minute_end.get()))
            bloc = {
                date_begin: [
                [
                    self.entry_hour_begin.get(),
                    self.entry_minute_begin.get(),  # Start time
                    self.entry_hour_end.get(),
                    self.entry_minute_end.get(),
                ],  # End time
        ]
    }
            try:
                meeting_time = get_duration(self.hours)

                # Check if the room is reservable
                result = verify_open_rooms(bloc)
                if result is not None:
                    self.text_room_reservable.config(state='normal')
                    self.text_room_reservable.delete(1.0, tk.END)
                    self.printTable(result, sep=' ', text=self.text_room_reservable)
                    self.text_room_reservable.config(state='disabled')
            except ValueError as e:
                self.text_room_reservable.config(state='normal')
                self.text_room_reservable.delete(1.0, tk.END)  # Clear the text widget before updating
                self.text_room_reservable.insert(tk.END, "Pas de salles disponibles pour cette période.")
                self.text_room_reservable.config(state='disabled')
        self.button_validate = ttk.Button(self.frame, text="Valider", command=validate)
        self.button_validate.grid(row=8, column=3, columnspan=2, padx=10, pady=10)

        self.button_cancel = ttk.Button(self.frame, text="Retour au menu principal", command=self.go_to_main_ui)
        self.button_cancel.grid(row=8, column=0, columnspan=2, padx=10, pady=10)

        return self.frame

def main(): 
    root = tk.Tk()
    app = Main_Window(root)
    root.mainloop()

if __name__ == '__main__':
    main()