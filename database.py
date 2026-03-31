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
    Fügt Beispielkategorien und Beispielfragen ein.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    # Alte Fragen löschen
    cursor.execute("DELETE FROM fragen")

    # Alte Kategorien löschen
    cursor.execute("DELETE FROM kategorien")

    # Neue Kategorien anlegen
    cursor.execute("INSERT INTO kategorien (name) VALUES (?)", ("Sport",))
    cursor.execute("INSERT INTO kategorien (name) VALUES (?)", ("Filme",))

    # Kategorien IDs holen
    cursor.execute("SELECT id FROM kategorien WHERE name = ?", ("Sport",))
    sport_id = cursor.fetchone()[0]

    cursor.execute("SELECT id FROM kategorien WHERE name = ?", ("Filme",))
    filme_id = cursor.fetchone()[0]

    # --- SPORT FRAGEN ---
    sport_fragen = [
        ("Für welchen Verein spielt Erling Haaland?", "Manchester City"),
        ("Welches Land gewann die Fußball-WM der Frauen 2023?", "Spanien"),
        ("In welcher Liga spielt LeBron James?", "NBA"),
        ("Welche Sportart ist Lionel Messis Hauptsport?", "Fußball"),
        ("Wie heißt die Netflix-Serie, die die Formel 1 weltweit populärer gemacht hat?", "Drive to Survive")
    ]

    for frage, antwort in sport_fragen:
        cursor.execute(
            "INSERT INTO fragen (kategorie_id, frage, antwort) VALUES (?, ?, ?)",
            (sport_id, frage, antwort)
        )

    # --- FILME FRAGEN ---
    film_fragen = [
        ("Wie heißt der pinke Blockbuster, der 2023 überall Thema war?", "Barbie"),
        ("Welche Schauspielerin spielt Wednesday Addams in der Netflix-Serie Wednesday?", "Jenna Ortega"),
        ("Welcher Film gewann 2023 den Oscar für den besten Film?", "Everything Everywhere All at Once"),
        ("Wie heißt der Schauspieler, der Ken in Barbie spielt?", "Ryan Gosling"),
        ("Welcher Animationsfilm über einen Klempner wurde 2023 ein riesiger Kinohit?", "The Super Mario Bros. Movie")
    ]

    for frage, antwort in film_fragen:
        cursor.execute(
            "INSERT INTO fragen (kategorie_id, frage, antwort) VALUES (?, ?, ?)",
            (filme_id, frage, antwort)
        )

    verbindung.commit()
    verbindung.close()
    
