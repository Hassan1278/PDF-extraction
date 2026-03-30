import json


def baue_prompt(text: str, schema: dict, seite_num: int, gesamt_seiten: int, letzter_fehler: str | None = None, ocr_verwendet: bool = False) -> str:
    schema_str = json.dumps(schema, indent=2)

    fehler_hinweis = ""
    if letzter_fehler:
        fehler_hinweis = f"\nDein letzter Versuch hatte diesen Fehler: {letzter_fehler}\nBitte korrigiere das.\n"

    bild_hinweis = ""
    if ocr_verwendet:
        bild_hinweis = "\nDer folgende Text wurde per OCR aus einem Scan extrahiert und kann Erkennungsfehler enthalten.\n"

    prompt = f"""Du bist ein Datenextraktions-Assistent.

Du verarbeitest Seite {seite_num + 1} von {gesamt_seiten}.
{fehler_hinweis}{bild_hinweis}
Extrahiere die Daten aus dem folgenden Text.
Beachte die Beschreibungen der Felder genau.
Felder mit "Zusammenfassung" oder "summary" sollst du selbst generieren.
Gib NUR die Werte zurück - kein Schema, keine Typen, keine Erklärungen.

Beispiel Antwort:
{{"name": "Max Mustermann", "datum": "01.01.2024"}}

Dein Schema:
{schema_str}

Text:
{text}

Antworte NUR mit dem JSON. Nur Feldnamen und Werte.
"""
    return prompt