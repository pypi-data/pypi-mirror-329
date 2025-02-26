import typer
from rich import print
from typing_extensions import Annotated

from ..utils.git_commands import LocalGitCommand

app = typer.Typer()


@app.command(
    name="create_local_repo_branch",
    help="创建一个新的 Git 分支",
    short_help="创建新分支"
)
def create_local_repo_branch(
        branch: Annotated[str, typer.Argument(
            help="新分支的名称",
            show_default=False,
        )],
        base_branch: Annotated[str, typer.Option(
            help="基础分支名称",
            show_default=True,
        )] = "master",
        is_global: Annotated[bool, typer.Option(
            "--global",
            "-g",
            help="是否在全局 Git 仓库中创建分支",
            show_default=True
        )] = False,
):
    """
    创建一个新的 Git 分支。
    Args:
        branch: 新分支的名称
        base_branch: 基础分支名称，默认为 master
        is_global: 是否为全局分支
    """
    git_cmd = LocalGitCommand(is_global)
    git_cmd.branch.create_branch(branch, base_branch)
    print(f"Branch {branch} created from {base_branch} in dir [bold red]{git_cmd.working_dir}[/bold red]")
