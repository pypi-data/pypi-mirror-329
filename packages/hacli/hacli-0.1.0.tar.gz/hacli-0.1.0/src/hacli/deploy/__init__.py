import typer

from . import services

app = typer.Typer()

app.add_typer(services.app)