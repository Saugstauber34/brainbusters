import sqlite3


DB_NAME = "brainbusters.db"


def verbindung_herstellen():
    """
    Stellt eine Verbindung zur SQLite-Datenbank her.
    """
    return sqlite3.connect(DB_NAME)


def datenbank_initialisieren():
    """
    Erstellt die Tabellen, falls sie noch nicht existieren.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS spieler (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            passwort TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS kategorien (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS fragen (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kategorie_id INTEGER NOT NULL,
            frage TEXT NOT NULL,
            antwort TEXT NOT NULL,
            FOREIGN KEY (kategorie_id) REFERENCES kategorien(id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ergebnisse (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spieler_id INTEGER NOT NULL,
            punkte INTEGER NOT NULL,
            FOREIGN KEY (spieler_id) REFERENCES spieler(id)
        )
    """)

    verbindung.commit()
    verbindung.close()


def testdaten_einfuegen():
    """
    Fügt Beispielkategorien und Beispielfragen ein, falls noch keine vorhanden sind.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("SELECT COUNT(*) FROM kategorien")
    anzahl_kategorien = cursor.fetchone()[0]

    if anzahl_kategorien == 0:
        cursor.execute("INSERT INTO kategorien (name) VALUES (?)", ("Allgemeinwissen",))
        cursor.execute("INSERT INTO kategorien (name) VALUES (?)", ("Informatik",))

        cursor.execute("SELECT id FROM kategorien WHERE name = ?", ("Allgemeinwissen",))
        allgemeinwissen_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM kategorien WHERE name = ?", ("Informatik",))
        informatik_id = cursor.fetchone()[0]

        fragen = [
            (allgemeinwissen_id, "Was ist die Hauptstadt von Deutschland?", "berlin"),
            (allgemeinwissen_id, "Wie viele Tage hat eine Woche?", "7"),
            (informatik_id, "Wofür steht CPU?", "central processing unit"),
            (informatik_id, "Welche Zahl besteht aus den Ziffern 0 und 1?", "binär")
        ]

        cursor.executemany(
            "INSERT INTO fragen (kategorie_id, frage, antwort) VALUES (?, ?, ?)",
            fragen
        )

    verbindung.commit()
    verbindung.close()
    