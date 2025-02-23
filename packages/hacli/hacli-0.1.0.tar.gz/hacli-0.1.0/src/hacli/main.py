import typer
from . import deploy

app = typer.Typer()

# app.registered_commands

# @app.callback()
# def callback():
#     """
#     Awesome Portal Gun
#     """


# @app.command()
# def shoot():
#     """
#     Shoot the portal gun
#     """
#     typer.echo("Shooting portal gun")


# @app.command()
# def load():
#     """
#     Load the portal gun
#     """
#     typer.echo("Loading portal gun")


app.add_typer(deploy.app)
