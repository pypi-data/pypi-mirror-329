import typer

from .rephraser import RephraseError, rephrase_text

app = typer.Typer()


@app.command()
def rephrase(
    text: str = typer.Argument(..., help="Text to rephrase"),
    style: str = typer.Option("normal", help="Style: normal, casual, formal, academic"),
) -> None:
    """Rephrase text in a specified style."""
    try:
        result = rephrase_text(text, style)
        typer.echo(result)
    except RephraseError as e:
        typer.echo(f"Error: {e}", err=True)
        raise typer.Exit(code=1) from e


if __name__ == "__main__":
    app()
