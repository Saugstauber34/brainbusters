import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import datenbank_initialisieren
from account import registrieren, einloggen


def test_registrieren_erfolgreich():
    """
    Testet, ob ein neuer Benutzer erfolgreich registriert werden kann.
    """
    datenbank_initialisieren()

    name = "testuser_123"
    passwort = "geheim"

    # Vorher evtl. alten Testbenutzer löschen
    verbindung = sqlite3.connect("brainbusters.db")
    cursor = verbindung.cursor()
    cursor.execute("DELETE FROM spieler WHERE name = ?", (name,))
    verbindung.commit()
    verbindung.close()

    ergebnis = registrieren(name, passwort)

    assert ergebnis is True


def test_einloggen_erfolgreich():
    """
    Testet, ob ein Benutzer sich erfolgreich einloggen kann.
    """
    datenbank_initialisieren()

    name = "loginuser_123"
    passwort = "testpasswort"

    verbindung = sqlite3.connect("brainbusters.db")
    cursor = verbindung.cursor()
    cursor.execute("DELETE FROM spieler WHERE name = ?", (name,))
    cursor.execute(
        "INSERT INTO spieler (name, passwort) VALUES (?, ?)",
        (name, passwort)
    )
    verbindung.commit()
    verbindung.close()

    spieler = einloggen(name, passwort)

    assert spieler is not None
    assert spieler[1] == name
    