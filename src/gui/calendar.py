import tkinter as tk
from tkinter import ttk
from datetime import datetime, timedelta

DAYS_LABELS = ['L', 'M', 'M', 'J', 'V', 'S', 'D']
HOURS = list(range(7, 19))  # 07:00 à 18:00

# Exemple de dictionnaire de réservations
reservations = {
    "13/05/2025": [[9, 0, 10, 30], [14, 0, 15, 15]],
    "14/05/2025": [[11, 0, 12, 0]],
}

# Obtenir le lundi de la semaine courante d'une date
def get_monday(date):
    return date - timedelta(days=date.weekday())


def create_week_view(root, reservations_dict):
    today = datetime.today()
    monday = get_monday(today)

    frame = ttk.Frame(root)
    frame.grid(row=0, column=0, sticky='nsew')

    # En-tête des jours
    day_date_map = {}
    for i, day_offset in enumerate(range(7)):
        date = monday + timedelta(days=day_offset)
        day_label = f"{DAYS_LABELS[i]}\n{date.strftime('%d/%m')}"
        day_date_map[date.strftime('%d/%m/%Y')] = i + 1  # colonne correspondante
        label = ttk.Label(frame, text=day_label, borderwidth=1, relief="solid", anchor='center')
        label.grid(row=0, column=i + 1, sticky='nsew')

    # Affichage des heures
    for h_index, hour in enumerate(HOURS, start=1):
        hour_str = f"{hour:02d}:00"
        label = ttk.Label(frame, text=hour_str, borderwidth=1, relief="solid", anchor='center', width=10)
        label.grid(row=h_index, column=0, sticky='nsew')

    # Créer un canevas pour afficher les événements à taille variable
    canvas = tk.Canvas(frame)
    canvas.grid(row=1, column=1, columnspan=7, rowspan=len(HOURS), sticky='nsew')

    cell_height = 60  # 1 heure = 60 pixels
    cell_width = 100

    # Affichage des réservations
    for date_str, slots in reservations_dict.items():
        if date_str in day_date_map:
            col_index = day_date_map[date_str]
            for slot in slots:
                h_start, m_start, h_end, m_end = slot
                start_time = h_start + m_start / 60
                end_time = h_end + m_end / 60
                duration = end_time - start_time

                # Calcule la position verticale
                y_start = (start_time - 7) * cell_height
                height = duration * cell_height

                event_frame = tk.Frame(canvas, bg="gray", highlightbackground="black", highlightthickness=1)
                canvas.create_window((col_index - 1) * cell_width, y_start, anchor="nw",
                                     window=event_frame, width=cell_width, height=height)
                tk.Label(event_frame, text=f"{h_start:02d}:{m_start:02d}-{h_end:02d}:{m_end:02d}",
                         fg='white', bg='gray').pack(fill='both', expand=True)

    # Règles de redimensionnement
    for i in range(8):
        frame.columnconfigure(i, weight=1)
    for i in range(len(HOURS) + 1):
        frame.rowconfigure(i, weight=1)


# Fenêtre principale
root = tk.Tk()
root.title("Calendrier Hebdomadaire avec Réservations Dynamiques")

create_week_view(root, reservations)

root.mainloop()