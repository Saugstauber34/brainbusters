import tkinter as tk
from tkinter import messagebox

from database import datenbank_initialisieren, testdaten_einfuegen, verbindung_herstellen
from achievements import achievements_tabelle_erstellen, achievement_vergeben
from account import registrieren, einloggen
from models import Spieler
from api import fragen_von_api_laden


aktueller_spieler = None
fragen_liste = []
aktuelle_frage_index = 0
punkte = 0
quiz_typ = "lokal"


def fragen_fuer_kategorie_laden(kategorie_id):
    """
    Lädt alle Fragen einer Kategorie aus der Datenbank.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "SELECT frage, antwort FROM fragen WHERE kategorie_id = ?",
        (kategorie_id,)
    )
    daten = cursor.fetchall()

    verbindung.close()
    return daten


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


def ergebnis_speichern_gui(spieler_id, punktzahl):
    """
    Speichert das Ergebnis des Spielers in der Datenbank.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "INSERT INTO ergebnisse (spieler_id, punkte) VALUES (?, ?)",
        (spieler_id, punktzahl)
    )

    verbindung.commit()
    verbindung.close()


def rangliste_laden():
    """
    Lädt die Rangliste aus der Datenbank.
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

    daten = cursor.fetchall()
    verbindung.close()
    return daten


def achievements_laden(spieler_id):
    """
    Lädt die Achievements eines Spielers.
    """
    verbindung = verbindung_herstellen()
    cursor = verbindung.cursor()

    cursor.execute(
        "SELECT titel FROM achievements WHERE spieler_id = ? ORDER BY titel",
        (spieler_id,)
    )

    daten = cursor.fetchall()
    verbindung.close()
    return daten


def registrieren_gui():
    """
    Registriert einen neuen Spieler über die GUI.
    """
    name = entry_name.get().strip()
    passwort = entry_passwort.get().strip()

    if not name or not passwort:
        messagebox.showwarning("Fehler", "Bitte Name und Passwort eingeben.")
        return

    if registrieren(name, passwort):
        messagebox.showinfo("Erfolg", "Registrierung erfolgreich.")
    else:
        messagebox.showerror("Fehler", "Benutzername existiert bereits.")


def einloggen_gui():
    """
    Loggt einen Spieler über die GUI ein.
    """
    global aktueller_spieler

    name = entry_name.get().strip()
    passwort = entry_passwort.get().strip()

    if not name or not passwort:
        messagebox.showwarning("Fehler", "Bitte Name und Passwort eingeben.")
        return

    spieler = einloggen(name, passwort)

    if spieler:
        aktueller_spieler = Spieler(spieler[0], spieler[1])
        label_status.config(text=f"Eingeloggt als: {aktueller_spieler.name}")
        messagebox.showinfo("Erfolg", f"Willkommen {aktueller_spieler.name}!")
    else:
        messagebox.showerror("Fehler", "Login fehlgeschlagen.")


def quiz_starten_gui():
    """
    Öffnet ein Fenster zur Auswahl einer lokalen Kategorie.
    """
    if aktueller_spieler is None:
        messagebox.showwarning("Fehler", "Bitte zuerst einloggen.")
        return

    kategorien = kategorien_laden()

    fenster_kategorien = tk.Toplevel(root)
    fenster_kategorien.title("Kategorie auswählen")
    fenster_kategorien.geometry("300x250")

    tk.Label(
        fenster_kategorien,
        text="Kategorie auswählen",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    for kategorie_id, name in kategorien:
        tk.Button(
            fenster_kategorien,
            text=name,
            width=20,
            command=lambda kid=kategorie_id, win=fenster_kategorien: quiz_vorbereiten(kid, win)
        ).pack(pady=5)


def quiz_vorbereiten(kategorie_id, fenster_kategorien):
    """
    Bereitet ein lokales Quiz vor.
    """
    global fragen_liste, aktuelle_frage_index, punkte, quiz_typ

    quiz_typ = "lokal"
    fenster_kategorien.destroy()

    fragen_liste = fragen_fuer_kategorie_laden(kategorie_id)
    aktuelle_frage_index = 0
    punkte = 0

    if not fragen_liste:
        messagebox.showwarning("Hinweis", "In dieser Kategorie sind keine Fragen vorhanden.")
        return

    frage_anzeigen()


def online_quiz_starten_gui():
    """
    Startet ein Online-Quiz mit Fragen aus der API.
    """
    global fragen_liste, aktuelle_frage_index, punkte, quiz_typ

    if aktueller_spieler is None:
        messagebox.showwarning("Fehler", "Bitte zuerst einloggen.")
        return

    quiz_typ = "api"

    api_fragen = fragen_von_api_laden(5)

    fragen_liste = []
    for eintrag in api_fragen:
        fragen_liste.append((eintrag["frage"], eintrag["antwort"]))

    aktuelle_frage_index = 0
    punkte = 0

    if not fragen_liste:
        messagebox.showwarning("Hinweis", "Es konnten keine Online-Fragen geladen werden.")
        return

    frage_anzeigen()


def frage_anzeigen():
    """
    Zeigt die aktuelle Frage im GUI-Fenster.
    """
    global quiz_fenster, entry_antwort

    if aktuelle_frage_index >= len(fragen_liste):
        quiz_beenden()
        return

    frage_text, _ = fragen_liste[aktuelle_frage_index]

    quiz_fenster = tk.Toplevel(root)
    quiz_fenster.title("BrainBusters Quiz")
    quiz_fenster.geometry("500x250")

    tk.Label(
        quiz_fenster,
        text=f"Frage {aktuelle_frage_index + 1} von {len(fragen_liste)}",
        font=("Arial", 10)
    ).pack(pady=10)

    tk.Label(
        quiz_fenster,
        text=frage_text,
        wraplength=450,
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    entry_antwort = tk.Entry(quiz_fenster, width=40)
    entry_antwort.pack(pady=10)

    tk.Button(
        quiz_fenster,
        text="Antwort prüfen",
        command=antwort_pruefen
    ).pack(pady=10)


def antwort_pruefen():
    """
    Prüft die eingegebene Antwort und springt zur nächsten Frage.
    """
    global aktuelle_frage_index, punkte

    user_antwort = entry_antwort.get().strip().lower()
    _, richtige_antwort = fragen_liste[aktuelle_frage_index]

    if user_antwort == richtige_antwort.lower():
        punkte += 1
        messagebox.showinfo("Ergebnis", "Richtig ✅")
    else:
        messagebox.showinfo("Ergebnis", f"Falsch ❌\nRichtige Antwort: {richtige_antwort}")

    quiz_fenster.destroy()
    aktuelle_frage_index += 1
    frage_anzeigen()


def quiz_beenden():
    """
    Beendet das Quiz, speichert das Ergebnis und vergibt Achievements.
    """
    global quiz_typ

    aktueller_spieler.punkte_setzen(punkte)
    ergebnis_speichern_gui(aktueller_spieler.spieler_id, aktueller_spieler.punkte)

    achievement_vergeben(aktueller_spieler.spieler_id, "Erstes Spiel")

    if quiz_typ == "api":
        achievement_vergeben(aktueller_spieler.spieler_id, "Online-Profi")

    if aktueller_spieler.punkte == len(fragen_liste):
        achievement_vergeben(aktueller_spieler.spieler_id, "Perfekt")

    messagebox.showinfo(
        "Quiz beendet",
        f"{aktueller_spieler.name} hat {aktueller_spieler.punkte} von {len(fragen_liste)} Punkten erreicht."
    )


def rangliste_gui():
    """
    Zeigt die Rangliste in einem Fenster an.
    """
    daten = rangliste_laden()

    fenster_rangliste = tk.Toplevel(root)
    fenster_rangliste.title("Rangliste")
    fenster_rangliste.geometry("350x300")

    tk.Label(
        fenster_rangliste,
        text="Rangliste",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    if not daten:
        tk.Label(fenster_rangliste, text="Noch keine Einträge vorhanden.").pack(pady=10)
        return

    for platz, (name, punktzahl) in enumerate(daten, start=1):
        tk.Label(
            fenster_rangliste,
            text=f"{platz}. {name} - {punktzahl} Punkte",
            anchor="w"
        ).pack(fill="x", padx=20, pady=2)


def achievements_gui():
    """
    Zeigt die Achievements des eingeloggten Spielers in einem Fenster an.
    """
    if aktueller_spieler is None:
        messagebox.showwarning("Fehler", "Bitte zuerst einloggen.")
        return

    daten = achievements_laden(aktueller_spieler.spieler_id)

    fenster_achievements = tk.Toplevel(root)
    fenster_achievements.title("Achievements")
    fenster_achievements.geometry("350x250")

    tk.Label(
        fenster_achievements,
        text="Deine Achievements",
        font=("Arial", 14, "bold")
    ).pack(pady=10)

    if not daten:
        tk.Label(
            fenster_achievements,
            text="Noch keine Achievements freigeschaltet."
        ).pack(pady=10)
        return

    for (titel,) in daten:
        tk.Label(
            fenster_achievements,
            text=f"🏅 {titel}",
            anchor="w"
        ).pack(fill="x", padx=20, pady=2)


# Datenbank vorbereiten
datenbank_initialisieren()
testdaten_einfuegen()
achievements_tabelle_erstellen()

# Hauptfenster
root = tk.Tk()
root.title("BrainBusters")
root.geometry("450x450")

tk.Label(root, text="BrainBusters", font=("Arial", 18, "bold")).pack(pady=15)

tk.Label(root, text="Benutzername").pack()
entry_name = tk.Entry(root, width=30)
entry_name.pack(pady=5)

tk.Label(root, text="Passwort").pack()
entry_passwort = tk.Entry(root, width=30, show="*")
entry_passwort.pack(pady=5)

tk.Button(root, text="Registrieren", width=20, command=registrieren_gui).pack(pady=8)
tk.Button(root, text="Einloggen", width=20, command=einloggen_gui).pack(pady=8)

tk.Label(root, text="").pack()

tk.Button(root, text="Quiz starten", width=20, command=quiz_starten_gui).pack(pady=8)
tk.Button(root, text="Online Quiz (API)", width=20, command=online_quiz_starten_gui).pack(pady=8)
tk.Button(root, text="Rangliste anzeigen", width=20, command=rangliste_gui).pack(pady=8)
tk.Button(root, text="Achievements anzeigen", width=20, command=achievements_gui).pack(pady=8)

label_status = tk.Label(root, text="Nicht eingeloggt", fg="blue")
label_status.pack(pady=15)

root.mainloop()
