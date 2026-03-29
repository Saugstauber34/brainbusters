import requests


def fragen_von_api_laden(anzahl=5):
    """
    Lädt Quizfragen von der Open Trivia DB API.
    """
    url = f"https://opentdb.com/api.php?amount={anzahl}&type=multiple"

    response = requests.get(url)
    daten = response.json()

    fragen_liste = []

    for item in daten["results"]:
        frage = item["question"]
        richtige_antwort = item["correct_answer"]

        fragen_liste.append({
            "frage": frage,
            "antwort": richtige_antwort
        })

    return fragen_liste
