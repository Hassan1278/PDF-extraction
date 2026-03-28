import json
def baue_prompt(text: str, schema: dict) -> str:
    schema_str = json.dumps(schema, indent=2)
    
    prompt = f"""Du bist ein Datenextraktions-Assistent.

Extrahiere die Daten aus dem folgenden Text.
Gib NUR die Werte zurück - kein Schema, keine Typen, keine Erklärungen.

Beispiel Schema:
{{"name": {{"type": "string"}}, "betrag": {{"type": "number"}}}}

Beispiel Antwort:
{{"name": "Max Mustermann", "betrag": 99.99}}

Dein Schema:
{schema_str}

Text:
{text}

Antworte NUR mit dem JSON. Nur Feldnamen und Werte.
"""
    return prompt