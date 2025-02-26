import typer
from typing_extensions import Annotated

from rich import print
from ..utils.git_commands import LocalGitCommand

app = typer.Typer()


#  TODO to complete it
@app.command(name="create_local_repo_branch")
def create_local_repo_branch(
    branch: str = typer.Argument(..., help="The branch name (required)"),
    base_branch: str = typer.Option("master", help="The base branch (default: master)"),
    is_global: Annotated[bool, typer.Option("--global", help="Whether the branch is global")] = False,
    push: Annotated[bool, typer.Option("--push", help="Whether to push the branch after creation")] = False
):
    command = LocalGitCommand(is_global)
    command.create_branch(branch, base_branch)
    # if push:
    #     command.push_branch(branch)
    print(f"Branch '{branch}' created from '{base_branch}' with global={is_global} and push={push}")
