import tkinter as tk
from datetime import datetime, timedelta

# === CONFIGURATION ===
CELL_WIDTH = 100
CELL_HEIGHT = 50
HOURS = list(range(7, 19))  # De 7h à 18h
DAYS = ["L", "M", "M", "J", "V", "S", "D"]
LEFT_OFFSET = CELL_WIDTH  # Pour laisser la colonne des heures

# === FONCTION PRINCIPALE D'AFFICHAGE ===
def afficher_semaine(root, reservations_dict, semaine_debut):
    for widget in root.winfo_children():
        widget.destroy()

    # Frame principale
    main_frame = tk.Frame(root, bg="lightgray")
    main_frame.pack(fill="both", expand=True)

    # === EN-TÊTES DES JOURS ===
    for i in range(7):
        date = semaine_debut + timedelta(days=i)
        jour = DAYS[i]
        label = tk.Label(main_frame, text=f"{jour}\n{date.strftime('%d/%m')}", bg="white", borderwidth=1, relief="solid")
        label.place(x=LEFT_OFFSET + i * CELL_WIDTH, y=0, width=CELL_WIDTH, height=CELL_HEIGHT)

    # === HEURES SUR LA GAUCHE ===
    for i, h in enumerate(HOURS):
        label = tk.Label(main_frame, text=f"{h:02d}:00", bg="white", borderwidth=1, relief="solid")
        label.place(x=0, y=(i + 1) * CELL_HEIGHT, width=CELL_WIDTH, height=CELL_HEIGHT)

    # === GRILLE VIDE ===
    for i in range(7):  # jours
        for j in range(len(HOURS)):  # heures
            label = tk.Label(main_frame, bg="#dcdcdc", borderwidth=1, relief="solid")
            label.place(x=LEFT_OFFSET + i * CELL_WIDTH, y=(j + 1) * CELL_HEIGHT, width=CELL_WIDTH, height=CELL_HEIGHT)

    # === RÉSERVATIONS ===
    day_date_map = {
        (semaine_debut + timedelta(days=i)).strftime("%d/%m/%Y"): i for i in range(7)
    }

    for date_str, slots in reservations_dict.items():
        if date_str in day_date_map:
            col = day_date_map[date_str]
            for slot in slots:
                h1, m1, h2, m2 = slot
                start = h1 + m1 / 60
                end = h2 + m2 / 60
                duration = end - start

                y = (start - 7) * CELL_HEIGHT
                height = duration * CELL_HEIGHT
                x = LEFT_OFFSET + col * CELL_WIDTH

                label = tk.Label(main_frame, text=f"{h1:02d}:{m1:02d}-{h2:02d}:{m2:02d}",
                                 bg="gray", fg="white", borderwidth=1, relief="raised")
                label.place(x=x, y=y + CELL_HEIGHT, width=CELL_WIDTH, height=height)

# === EXEMPLE D'UTILISATION ===
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Vue Semaine Réservations")
    root.geometry("900x700")

    # Exemple de réservations
    reservations = {
        "12/05/2025": [[9, 0, 10, 30], [16, 30, 17, 15]],
        "13/05/2025": [[11, 0, 12, 0]],
        # Ajoute d'autres jours si besoin
    }

    # Date du lundi de la semaine courante
    aujourd_hui = datetime.strptime("13/05/2025", "%d/%m/%Y")  # Tu peux mettre datetime.today()
    lundi = aujourd_hui - timedelta(days=aujourd_hui.weekday())

    afficher_semaine(root, reservations, lundi)

    root.mainloop()
