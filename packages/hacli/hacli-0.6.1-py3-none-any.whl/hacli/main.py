import sys
import warnings

import typer

from . import deploy
from . import git
from . import image
from . import tag
from .utils.envs import load_yaml_env_vars



def start():
    warnings.filterwarnings("ignore")
    sys.tracebacklimit = 0

    app = typer.Typer(pretty_exceptions_show_locals=False)
    app.add_typer(deploy.app, name="deploy")
    app.add_typer(tag.app, name="tag")
    app.add_typer(git.app, name="git")
    app.add_typer(image.app, name="image")

    try:
        load_yaml_env_vars()
        app()
    except Exception as e:
        typer.secho(e, err=True, bold=True, fg=typer.colors.RED)
        sys.exit(1)
