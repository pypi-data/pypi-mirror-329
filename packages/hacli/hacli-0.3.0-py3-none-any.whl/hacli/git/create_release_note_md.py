import os
from string import Template

import typer
from git import GitCommandError
from rich import print

from ..utils.git_commands import LocalGitCommand

app = typer.Typer()

default_services = [
    "product-management",
    "service-management",
    "vehicle-management",
    "user-management",
    "system"
]

from rich import print


@app.command(name="create_release_note_md")
def create_release_note_md(pre_release: str, cur_release: str):
    command = LocalGitCommand(True).repo

    #  TODO services change requests needed...
    str_list = []
    for service in default_services:
        commands = (
            Template(os.environ["GIT_RELEASE_NOTE_COMMAND_CONFIGURATION"])
            .safe_substitute(service=service,
                             pre_release=pre_release,
                             cur_release=cur_release)
        )
        try:
            str_list.append(f"\n### {service}\n")
            log_output = command.git.execute(command=commands, shell=True)
            str_list.append(log_output)
        except GitCommandError as e:
            str_list.append(e.stderr)

    final_str = '\n'.join(str_list)
    print(final_str)
