import sys
import os
import sqlite3

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from database import datenbank_initialisieren
from scoreboard import ergebnis_speichern, rangliste_anzeigen


DB_NAME = "brainbusters.db"


def testdaten_zuruecksetzen():
    """
    Löscht Testdaten aus der Datenbank, damit die Tests sauber starten.
    """
    verbindung = sqlite3.connect(DB_NAME)
    cursor = verbindung.cursor()

    cursor.execute("DELETE FROM ergebnisse")
    cursor.execute("DELETE FROM spieler")

    # Testspieler neu anlegen
    cursor.execute(
        "INSERT INTO spieler (id, name, passwort) VALUES (?, ?, ?)",
        (1, "Ali", "test")
    )
    cursor.execute(
        "INSERT INTO spieler (id, name, passwort) VALUES (?, ?, ?)",
        (2, "Mila", "test")
    )
    cursor.execute(
        "INSERT INTO spieler (id, name, passwort) VALUES (?, ?, ?)",
        (3, "Can", "test")
    )

    verbindung.commit()
    verbindung.close()


def test_ergebnis_speichern():
    """
    Testet, ob ein Ergebnis korrekt in der Datenbank gespeichert wird.
    """
    datenbank_initialisieren()
    testdaten_zuruecksetzen()

    ergebnis_speichern(1, 2)

    verbindung = sqlite3.connect(DB_NAME)
    cursor = verbindung.cursor()
    cursor.execute("SELECT spieler_id, punkte FROM ergebnisse WHERE spieler_id = 1")
    ergebnis = cursor.fetchone()
    verbindung.close()

    assert ergebnis is not None
    assert ergebnis[0] == 1
    assert ergebnis[1] == 2


def test_mehrere_ergebnisse_speichern():
    """
    Testet, ob mehrere Ergebnisse korrekt gespeichert werden.
    """
    datenbank_initialisieren()
    testdaten_zuruecksetzen()

    ergebnis_speichern(1, 2)
    ergebnis_speichern(2, 3)

    verbindung = sqlite3.connect(DB_NAME)
    cursor = verbindung.cursor()
    cursor.execute("SELECT COUNT(*) FROM ergebnisse")
    anzahl = cursor.fetchone()[0]
    verbindung.close()

    assert anzahl == 2


def test_rangliste_sortierte_ausgabe(capsys):
    """
    Testet, ob die Rangliste absteigend nach Punkten ausgegeben wird.
    """
    datenbank_initialisieren()
    testdaten_zuruecksetzen()

    ergebnis_speichern(1, 2)  # Ali
    ergebnis_speichern(2, 5)  # Mila
    ergebnis_speichern(3, 3)  # Can

    rangliste_anzeigen()

    captured = capsys.readouterr()
    ausgabe = captured.out

    assert "1. Mila - 5 Punkte" in ausgabe
    assert "2. Can - 3 Punkte" in ausgabe
    assert "3. Ali - 2 Punkte" in ausgabe
    