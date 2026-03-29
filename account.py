from database import verbindung_herstellen


def registrieren(name, passwort):
    """
    Registriert einen neuen Spieler.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    try:
        cursor.execute(
            "INSERT INTO spieler (name, passwort) VALUES (?, ?)",
            (name, passwort)
        )
        verbindung.commit()
        return True
    except:
        return False
    finally:
        verbindung.close()


def einloggen(name, passwort):
    """
    Prüft, ob Login-Daten korrekt sind.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "SELECT id, name FROM spieler WHERE name = ? AND passwort = ?",
        (name, passwort)
    )

    spieler = cursor.fetchone()
    verbindung.close()

    return spieler
