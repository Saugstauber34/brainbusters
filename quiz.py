from database import verbindung_herstellen
from api import fragen_von_api_laden


def hilfe_anzeigen():
    """
    Zeigt dem Spieler die Steuerungshilfe an.
    """
    print("\n--- Hilfe ---")
    print("1 = Quiz spielen")
    print("2 = Rangliste anzeigen")
    print("3 = Hilfe anzeigen")
    print("4 = Online Quiz (API)")
    print("5 = Mehrspielermodus")
    print("6 = Achievements anzeigen")
    print("7 = Beenden")


def kategorien_laden():
    """
    Lädt alle Kategorien aus der Datenbank.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute("SELECT id, name FROM kategorien")
    kategorien = cursor.fetchall()

    verbindung.close()
    return kategorien


def kategorien_anzeigen():
    """
    Gibt alle Kategorien aus der Datenbank aus.
    """
    kategorien = kategorien_laden()

    print("\nVerfügbare Kategorien:")
    for kategorie_id, name in kategorien:
        print(f"{kategorie_id} - {name}")


def quiz_spielen(kategorie_id):
    """
    Führt das Quiz für eine gewählte Kategorie aus.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "SELECT frage, antwort FROM fragen WHERE kategorie_id = ?",
        (kategorie_id,)
    )
    fragen = cursor.fetchall()
    verbindung.close()

    punkte = 0

    for frage, antwort in fragen:
        print("\n" + frage)
        user_antwort = input("Deine Antwort: ").strip().lower()

        if user_antwort == antwort.lower():
            print("Richtig ✅")
            punkte += 1
        else:
            print(f"Falsch ❌ Richtige Antwort: {antwort}")

    return punkte


def quiz_spielen_api():
    """
    Führt ein Online-Quiz mit Fragen aus der API aus.
    """
    fragen = fragen_von_api_laden(5)
    punkte = 0

    for eintrag in fragen:
        print("\n" + eintrag["frage"])
        user_antwort = input("Deine Antwort: ").strip().lower()

        if user_antwort == eintrag["antwort"].lower():
            print("Richtig ✅")
            punkte += 1
        else:
            print(f"Falsch ❌ Richtige Antwort: {eintrag['antwort']}")

    return punkte
