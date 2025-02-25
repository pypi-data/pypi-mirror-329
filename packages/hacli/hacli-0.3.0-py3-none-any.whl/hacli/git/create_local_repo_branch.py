import typer
from typing_extensions import Annotated

from ..utils.git_commands import LocalGitCommand

app = typer.Typer()


#  TODO to complete it
@app.command(name="create_local_repo_branch")
def create_local_repo_branch(branch: str,
                             base_branch: str = "master",
                             is_global: Annotated[bool, typer.Option("--global")] = False,
                             push: Annotated[bool, typer.Option("--push")] = False):
    command = LocalGitCommand(is_global)
    command.create_branch(branch, base_branch)
