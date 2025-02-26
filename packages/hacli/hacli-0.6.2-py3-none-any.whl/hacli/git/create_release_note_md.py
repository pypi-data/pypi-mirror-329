import os
from string import Template

import typer
from git import GitCommandError
from rich import print
from typing_extensions import Annotated

from ..utils.git_commands import LocalGitCommand

app = typer.Typer()

default_services = [
    "product-management",
    "service-management",
    "vehicle-management",
    "user-management",
    "system"
]


@app.command(name="create_release_note_md",
             help="生成版本发布说明文档，自动收集指定服务在两个版本之间的所有提交记录",
             short_help="生成版本发布说明文档")
def create_release_note_md(
        pre_release: Annotated[str, typer.Argument(help="前一个版本号，例如：v1.0.0")],
        cur_release: Annotated[str, typer.Argument(help="当前版本号，例如：v1.1.0")]
):
    """
        生成版本发布说明文档（Release Notes）。

        此命令会自动收集指定服务在两个版本之间的所有 Git 提交记录，并生成一个格式化的 Markdown 文档。
        文档按服务进行分类，每个服务的提交记录都会单独列出。

        Args:
            pre_release: 前一个版本的标签名称（例如：v1.0.0）
            cur_release: 当前版本的标签名称（例如：v1.1.0）

        环境变量:
            GIT_RELEASE_NOTE_COMMAND_CONFIGURATION: Git 命令模板，用于获取提交记录
                模板变量：
                - ${service}: 服务名称
                - ${pre_release}: 前一个版本号
                - ${cur_release}: 当前版本号

        示例:
            $ hacli git create_release_note_md v1.0.0 v1.1.0

        注意:
            - 需要确保环境变量 GIT_RELEASE_NOTE_COMMAND_CONFIGURATION 已正确设置
            - 该命令会在全局 Git 仓库中执行
            - 如果某个服务获取提交记录失败，会显示错误信息但不会中断整个过程
    """

    command = LocalGitCommand(True).repo

    # TODO services change requests needed...
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
