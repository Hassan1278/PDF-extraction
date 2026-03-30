import json
import typer
from pathlib import Path

from src.doc_extract.pipeline import run_pipeline

app = typer.Typer()


@app.command()
def extract(
    pdf: Path = typer.Argument(..., help="Path to the PDF file"),
    schema: Path = typer.Argument(..., help="Path to the JSON schema file"),
):
    if not pdf.exists():
        typer.echo(f"Error: PDF not found: {pdf}")
        raise typer.Exit(1)

    if not schema.exists():
        typer.echo(f"Error: Schema not found: {schema}")
        raise typer.Exit(1)

    schema_dict = json.loads(schema.read_text())
    typer.echo(f"Processing: {pdf.name}...")

    result = run_pipeline(pdf, schema_dict)

    typer.echo(f"Valid: {result.valid}")
    typer.echo(f"Pages: {result.pages}")
    typer.echo(f"Data: {json.dumps(result.data, indent=2)}")

    if result.errors:
        typer.echo(f"Errors: {result.errors}")


if __name__ == "__main__":
    app()
