from database import datenbank_initialisieren, testdaten_einfuegen
from account import registrieren, einloggen
from quiz import hilfe_anzeigen, kategorien_anzeigen, quiz_spielen, quiz_spielen_api
from scoreboard import ergebnis_speichern, rangliste_anzeigen
from achievements import (
    achievements_tabelle_erstellen,
    achievement_vergeben,
    achievements_anzeigen
)
from models import Spieler


def login_oder_registrierung():
    """
    Fragt ab, ob sich der Benutzer einloggen oder registrieren möchte.
    """
    print("Willkommen bei BrainBusters!")
    print("1 - Registrieren")
    print("2 - Einloggen")

    auswahl = input("Bitte wählen: ").strip()

    if auswahl == "1":
        name = input("Neuer Benutzername: ").strip()
        passwort = input("Neues Passwort: ").strip()

        if registrieren(name, passwort):
            print("Registrierung erfolgreich.")
        else:
            print("Benutzername existiert bereits.")
        return None

    elif auswahl == "2":
        name = input("Benutzername: ").strip()
        passwort = input("Passwort: ").strip()

        spieler = einloggen(name, passwort)

        if spieler:
            print(f"Erfolgreich eingeloggt als {spieler[1]}")
            return spieler
        else:
            print("Login fehlgeschlagen.")
            return None

    else:
        print("Ungültige Eingabe.")
        return None


def mehrspieler_modus():
    """
    Lässt zwei Spieler nacheinander spielen und vergleicht ihre Ergebnisse.
    """
    print("\n--- Mehrspielermodus ---")
    print("Spieler 1 muss sich einloggen.")
    spieler1 = login_oder_registrierung()

    if not spieler1:
        print("Spieler 1 konnte nicht eingeloggt werden.")
        return

    print("\nSpieler 2 muss sich einloggen.")
    spieler2 = login_oder_registrierung()

    if not spieler2:
        print("Spieler 2 konnte nicht eingeloggt werden.")
        return

    print("\nVerfügbare Kategorien:")
    kategorien_anzeigen()

    try:
        kategorie_id = int(input("Kategorie-ID für beide Spieler: ").strip())
    except ValueError:
        print("Ungültige Eingabe.")
        return

    print(f"\n{spieler1[1]} ist jetzt dran.")
    punkte_spieler1 = quiz_spielen(kategorie_id)
    spieler1_objekt = Spieler(spieler1[0], spieler1[1])
    spieler1_objekt.punkte_setzen(punkte_spieler1)
    ergebnis_speichern(spieler1_objekt.spieler_id, spieler1_objekt.punkte)
    achievement_vergeben(spieler1_objekt.spieler_id, "Erstes Spiel")

    print(f"\n{spieler2[1]} ist jetzt dran.")
    punkte_spieler2 = quiz_spielen(kategorie_id)
    spieler2_objekt = Spieler(spieler2[0], spieler2[1])
    spieler2_objekt.punkte_setzen(punkte_spieler2)
    ergebnis_speichern(spieler2_objekt.spieler_id, spieler2_objekt.punkte)
    achievement_vergeben(spieler2_objekt.spieler_id, "Erstes Spiel")

    print("\n--- Ergebnis Mehrspielermodus ---")
    print(f"{spieler1_objekt.name}: {spieler1_objekt.punkte} Punkte")
    print(f"{spieler2_objekt.name}: {spieler2_objekt.punkte} Punkte")

    if spieler1_objekt.punkte > spieler2_objekt.punkte:
        print(f"Gewonnen hat: {spieler1_objekt.name} 🏆")
        achievement_vergeben(spieler1_objekt.spieler_id, "Mehrspieler-Sieger")
    elif spieler2_objekt.punkte > spieler1_objekt.punkte:
        print(f"Gewonnen hat: {spieler2_objekt.name} 🏆")
        achievement_vergeben(spieler2_objekt.spieler_id, "Mehrspieler-Sieger")
    else:
        print("Unentschieden 🤝")


def menue(spieler):
    """
    Hauptmenü nach dem Login.
    """
    while True:
        print("\n--- Hauptmenü ---")
        print("1 - Quiz spielen")
        print("2 - Rangliste anzeigen")
        print("3 - Hilfe anzeigen")
        print("4 - Online Quiz (API)")
        print("5 - Mehrspielermodus")
        print("6 - Achievements anzeigen")
        print("7 - Beenden")

        auswahl = input("Bitte wählen: ").strip()

        if auswahl == "1":
            kategorien_anzeigen()
            try:
                kategorie_id = int(input("Kategorie-ID eingeben: ").strip())
                punkte = quiz_spielen(kategorie_id)

                aktueller_spieler = Spieler(spieler[0], spieler[1])
                aktueller_spieler.punkte_setzen(punkte)

                print(f"\nSpiel beendet. {aktueller_spieler}")
                ergebnis_speichern(aktueller_spieler.spieler_id, aktueller_spieler.punkte)
                achievement_vergeben(aktueller_spieler.spieler_id, "Erstes Spiel")

                if aktueller_spieler.punkte >= 2:
                    achievement_vergeben(aktueller_spieler.spieler_id, "Perfekt")

            except ValueError:
                print("Bitte eine gültige Zahl eingeben.")

        elif auswahl == "2":
            rangliste_anzeigen()

        elif auswahl == "3":
            hilfe_anzeigen()

        elif auswahl == "4":
            punkte = quiz_spielen_api()

            aktueller_spieler = Spieler(spieler[0], spieler[1])
            aktueller_spieler.punkte_setzen(punkte)

            print(f"\nOnline-Quiz beendet. {aktueller_spieler}")
            ergebnis_speichern(aktueller_spieler.spieler_id, aktueller_spieler.punkte)
            achievement_vergeben(aktueller_spieler.spieler_id, "Erstes Spiel")
            achievement_vergeben(aktueller_spieler.spieler_id, "Online-Profi")

        elif auswahl == "5":
            mehrspieler_modus()

        elif auswahl == "6":
            achievements_anzeigen(spieler[0])

        elif auswahl == "7":
            print("Programm beendet.")
            break

        else:
            print("Ungültige Eingabe.")


def main():
    datenbank_initialisieren()
    testdaten_einfuegen()
    achievements_tabelle_erstellen()

    spieler = login_oder_registrierung()

    if spieler:
        menue(spieler)


if __name__ == "__main__":
    main()
    