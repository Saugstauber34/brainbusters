from database import verbindung_herstellen


def ergebnis_speichern(spieler_id, punkte):
    """
    Speichert das Ergebnis eines Spielers in der Datenbank.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "INSERT INTO ergebnisse (spieler_id, punkte) VALUES (?, ?)",
        (spieler_id, punkte)
    )

    verbindung.commit()
    verbindung.close()


def rangliste_anzeigen():
    """
    Gibt die Rangliste aus.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("""
        SELECT spieler.name, MAX(ergebnisse.punkte) as beste_punktzahl
        FROM ergebnisse
        JOIN spieler ON ergebnisse.spieler_id = spieler.id
        GROUP BY spieler.id
        ORDER BY beste_punktzahl DESC
    """)

    rangliste = cursor.fetchall()
    verbindung.close()

    print("\n--- Rangliste ---")

    if not rangliste:
        print("Noch keine Einträge vorhanden.")
        return

    for platz, (name, punkte) in enumerate(rangliste, start=1):
        print(f"{platz}. {name} - {punkte} Punkte")
        