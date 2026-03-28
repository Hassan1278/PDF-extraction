from src.doc_extract.inference.vllm_client import sende_anfrage

antwort = sende_anfrage("Sag nur: Hallo, ich funktioniere!")
print(antwort)