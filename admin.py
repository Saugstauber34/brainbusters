from database import verbindung_herstellen, datenbank_initialisieren, testdaten_einfuegen


def fragen_anzeigen():
    """
    Zeigt alle Fragen mit ID und Kategorie an.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("""
        SELECT fragen.id, kategorien.name, fragen.frage, fragen.antwort
        FROM fragen
        JOIN kategorien ON fragen.kategorie_id = kategorien.id
        ORDER BY fragen.id
    """)

    fragen = cursor.fetchall()
    verbindung.close()

    print("\n--- Fragenübersicht ---")
    if not fragen:
        print("Keine Fragen vorhanden.")
        return

    for frage_id, kategorie, frage, antwort in fragen:
        print(f"ID: {frage_id} | Kategorie: {kategorie}")
        print(f"Frage: {frage}")
        print(f"Antwort: {antwort}")
        print("-" * 40)


def kategorien_anzeigen():
    """
    Zeigt alle Kategorien an.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("SELECT id, name FROM kategorien ORDER BY id")
    kategorien = cursor.fetchall()

    verbindung.close()

    print("\n--- Kategorien ---")
    for kategorie_id, name in kategorien:
        print(f"{kategorie_id} - {name}")


def frage_hinzufuegen():
    """
    Fügt eine neue Frage hinzu.
    """
    kategorien_anzeigen()

    try:
        kategorie_id = int(input("Kategorie-ID: ").strip())
    except ValueError:
        print("Ungültige Kategorie-ID.")
        return

    frage = input("Neue Frage eingeben: ").strip()
    antwort = input("Richtige Antwort eingeben: ").strip()

    if not frage or not antwort:
        print("Frage und Antwort dürfen nicht leer sein.")
        return

    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "INSERT INTO fragen (kategorie_id, frage, antwort) VALUES (?, ?, ?)",
        (kategorie_id, frage, antwort)
    )

    verbindung.commit()
    verbindung.close()

    print("Frage erfolgreich hinzugefügt.")


def frage_bearbeiten():
    """
    Bearbeitet eine bestehende Frage.
    """
    fragen_anzeigen()

    try:
        frage_id = int(input("ID der Frage zum Bearbeiten: ").strip())
    except ValueError:
        print("Ungültige ID.")
        return

    neue_frage = input("Neue Frage: ").strip()
    neue_antwort = input("Neue Antwort: ").strip()

    if not neue_frage or not neue_antwort:
        print("Frage und Antwort dürfen nicht leer sein.")
        return

    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "UPDATE fragen SET frage = ?, antwort = ? WHERE id = ?",
        (neue_frage, neue_antwort, frage_id)
    )

    verbindung.commit()

    if cursor.rowcount == 0:
        print("Keine Frage mit dieser ID gefunden.")
    else:
        print("Frage erfolgreich bearbeitet.")

    verbindung.close()


def frage_loeschen():
    """
    Löscht eine Frage anhand der ID.
    """
    fragen_anzeigen()

    try:
        frage_id = int(input("ID der Frage zum Löschen: ").strip())
    except ValueError:
        print("Ungültige ID.")
        return

    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("DELETE FROM fragen WHERE id = ?", (frage_id,))
    verbindung.commit()

    if cursor.rowcount == 0:
        print("Keine Frage mit dieser ID gefunden.")
    else:
        print("Frage erfolgreich gelöscht.")

    verbindung.close()


def admin_menue():
    """
    Admin-Backend zur Verwaltung von Quizfragen.
    """
    while True:
        print("\n--- Admin-Backend ---")
        print("1 - Fragen anzeigen")
        print("2 - Frage hinzufügen")
        print("3 - Frage bearbeiten")
        print("4 - Frage löschen")
        print("5 - Beenden")

        auswahl = input("Bitte wählen: ").strip()

        if auswahl == "1":
            fragen_anzeigen()
        elif auswahl == "2":
            frage_hinzufuegen()
        elif auswahl == "3":
            frage_bearbeiten()
        elif auswahl == "4":
            frage_loeschen()
        elif auswahl == "5":
            print("Admin-Backend beendet.")
            break
        else:
            print("Ungültige Eingabe.")


# 🔥 WICHTIG: richtiger Startpunkt
if __name__ == "__main__":
    datenbank_initialisieren()
    testdaten_einfuegen()
    admin_menue()
    