import json

def baue_prompt(text: str, schema: dict, seite_num: int, gesamt_seiten: int) -> str:
    schema_str = json.dumps(schema, indent=2)

    prompt = f"""Du bist ein Datenextraktions-Assistent.

Du verarbeitest Seite {seite_num + 1} von {gesamt_seiten}.

Extrahiere die Daten aus dem folgenden Text.
Beachte die Beschreibungen der Felder genau.
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