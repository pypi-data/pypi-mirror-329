from typing import Annotated

import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(
    name="teardown_inactive_cluster",
    help="清理非活动集群",
    short_help="清理非活动集群"
)
def teardown_inactive_cluster(
        release: Annotated[str, typer.Argument(
            help="发布版本号",
            show_default=False,
            metavar="VERSION"
        )]
) -> None:
    """
    清理非活动集群的资源。

    此命令用于触发 Azure DevOps 流水线来清理非活动集群的所有资源。
    清理操作将移除指定版本的所有相关资源。

    Args:
        release: 要清理的版本号，例如 "v1.0.0"

    环境变量:
        DEPLOY_PIPELINES_TEARDOWN_INACTIVE_CLUSTER_NAME: 清理流水线名称
        DEPLOY_PIPELINES_TEARDOWN_INACTIVE_CLUSTER_PARAMETERS: 清理流水线参数配置

    Examples:
        清理指定版本的非活动集群：
            $ hacli deploy teardown_inactive_cluster v1.0.0

    注意:
        - 此操作将清理所有相关资源，请谨慎执行
        - 确保指定的版本号正确
        - 执行前请确保已正确设置所需的环境变量
    """
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_TEARDOWN_INACTIVE_CLUSTER_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_TEARDOWN_INACTIVE_CLUSTER_PARAMETERS")
