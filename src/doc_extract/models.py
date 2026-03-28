from pydantic import BaseModel

class SeiteInfo(BaseModel):
    seite: int
    zeichen: int
    bilder: int
    typ: str

class ExtractionErgebnis(BaseModel):
    request_id: str
    seiten: int
    valid: bool
    daten: dict
    fehler: list[str]
    retry_count: int