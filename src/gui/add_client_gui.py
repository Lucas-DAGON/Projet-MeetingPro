from src.controller.add_client import add_client

def add_client_gui(surname: str, name: str, email_address: str, client_id: int, clients: list) -> tuple:
    if not surname or not name or not email_address:
        return "Erreur: Tous les champs doivent être remplis.", client_id, clients
    client_id = len(clients) + 1
    clients.append(add_client(name, surname, email_address))
    return True, client_id, clients