import json
import typer
from pathlib import Path
from src.doc_extract.pipeline import run_pipeline

app = typer.Typer()

@app.command()
def extract(
    pdf: Path = typer.Argument(..., help="Pfad zur PDF Datei"),
    schema: Path = typer.Argument(..., help="Pfad zur JSON Schema Datei"),
):
    if not pdf.exists():
        typer.echo(f"Fehler: PDF nicht gefunden: {pdf}")
        raise typer.Exit(1)

    if not schema.exists():
        typer.echo(f"Fehler: Schema nicht gefunden: {schema}")
        raise typer.Exit(1)

    schema_dict = json.loads(schema.read_text())
    typer.echo(f"Verarbeite: {pdf.name}...")

    ergebnis = run_pipeline(pdf, schema_dict)

    typer.echo(f"Valid: {ergebnis.valid}")
    typer.echo(f"Seiten: {ergebnis.seiten}")
    typer.echo(f"Daten: {json.dumps(ergebnis.daten, indent=2)}")

    if ergebnis.fehler:
        typer.echo(f"Fehler: {ergebnis.fehler}")

if __name__ == "__main__":
    app()