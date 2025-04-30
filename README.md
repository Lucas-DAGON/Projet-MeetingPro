# Projet-MeetingPro
Graphical interface to reserve a room


# Modélisation UML des salles

## Description

Il existe trois types de salles : `Standard`, `Conférence`, et `Informatique`.  
Toutes héritent de la classe `Standard`.

---

## Diagramme de classes UML (représentation textuelle)

```plaintext
            +--------------------------------------+
            |               Standard               |
            +--------------------------------------+
            | - nom: String                        |
            | - nbPlaces: int                      |
            +--------------------------------------+
            | +tropDePersonnes(n: int): bool       |
            | +dureeReservationValide(): bool      |
            | +estDisponible(): bool               |
            | +disponibleAPartirDe(): int List[5]  |
            +--------------------------------------+
                                ^
                                |
              +----------------+------------------+
              |                                   |
    +--------------------------+           +----------------------+
    |        Conférence        |           |   Informatique       |
    +--------------------------+           +----------------------+
    |                          |           | - equipement : str   |
    +--------------------------+           +----------------------+
    | +tropPeuDeMonde(n): bool |           |                      |
    +--------------------------+           +----------------------+
```


