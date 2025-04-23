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
            | - debut: DateTime                    |
            | - fin: DateTime                      |
            +--------------------------------------+
            | +tropDePersonnes(n: int): bool       |
            | +dureeReservationValide(): bool      |
            +--------------------------------------+
                                ^
                                |
              +----------------+------------------+
              |                                   |
    +--------------------------+           +----------------------+
    |        Conférence        |           |   Informatique       |
    +--------------------------+           +----------------------+
    |                          |           | - avecPC: bool       |
    +--------------------------+           +----------------------+
    | +tropPeuDeMonde(n): bool |           |                      |
    +--------------------------+           +----------------------+
```


