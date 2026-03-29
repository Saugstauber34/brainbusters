class Spieler:
    """
    Repräsentiert einen Spieler mit ID, Name und Punktestand.
    """

    def __init__(self, spieler_id, name, punkte=0):
        self.spieler_id = spieler_id
        self.name = name
        self.punkte = punkte

    def punkte_setzen(self, punkte):
        """
        Setzt die Punktzahl des Spielers.
        """
        self.punkte = punkte

    def __str__(self):
        return f"{self.name} ({self.punkte} Punkte)"
    