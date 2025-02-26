import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(
    name="sync_global_repo",
    help="同步全局代码仓库",
    short_help="同步全局仓库"
)
def sync_global_repo() -> None:
    """
    同步全局代码仓库。

    此命令用于触发 Azure DevOps 流水线来同步全局代码仓库。
    默认使用 master 分支作为同步源。

    环境变量:
        DEPLOY_PIPELINES_SYNC_GLOBAL_REPO_NAME: 同步流水线名称
        DEPLOY_PIPELINES_SYNC_GLOBAL_REPO_PARAMETERS: 同步流水线参数配置
        PROJECT_GLOBAL_NAME: 全局项目名称
        PROJECT_GLOBAL_REPO: 全局仓库名称

    Examples:
        同步全局仓库：
            $ hacli deploy sync_global_repo

    注意:
        - 执行前请确保已正确设置所需的环境变量
        - 此操作将同步 master 分支的内容
        - 确保有足够的权限访问全局仓库
    """
    execute_pipeline(release="master",
                     pipeline_name_env_key="DEPLOY_PIPELINES_SYNC_GLOBAL_REPO_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_SYNC_GLOBAL_REPO_PARAMETERS",
                     project_name_env_key="PROJECT_GLOBAL_NAME",
                     project_repo_env_key="PROJECT_GLOBAL_REPO")
