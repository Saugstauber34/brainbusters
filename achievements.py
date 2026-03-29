from database import verbindung_herstellen


def achievements_tabelle_erstellen():
    """
    Erstellt die Tabelle für Achievements, falls sie noch nicht existiert.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS achievements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            spieler_id INTEGER NOT NULL,
            titel TEXT NOT NULL,
            UNIQUE(spieler_id, titel),
            FOREIGN KEY (spieler_id) REFERENCES spieler(id)
        )
    """)

    verbindung.commit()
    verbindung.close()


def achievement_vergeben(spieler_id, titel):
    """
    Vergibt einem Spieler ein Achievement, falls es noch nicht vorhanden ist.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    try:
        cursor.execute(
            "INSERT INTO achievements (spieler_id, titel) VALUES (?, ?)",
            (spieler_id, titel)
        )
        verbindung.commit()
        print(f"🏅 Neues Achievement freigeschaltet: {titel}")
    except:
        pass
    finally:
        verbindung.close()


def achievements_anzeigen(spieler_id):
    """
    Zeigt alle Achievements eines Spielers an.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "SELECT titel FROM achievements WHERE spieler_id = ? ORDER BY titel",
        (spieler_id,)
    )
    eintraege = cursor.fetchall()
    verbindung.close()

    print("\n--- Deine Achievements ---")
    if not eintraege:
        print("Noch keine Achievements freigeschaltet.")
        return

    for (titel,) in eintraege:
        print(f"- {titel}")
        