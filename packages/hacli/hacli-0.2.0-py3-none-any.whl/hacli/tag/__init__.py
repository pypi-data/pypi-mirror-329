import typer

from . import get_global_rollout_status

app = typer.Typer()

app.add_typer(get_global_rollout_status.app)
