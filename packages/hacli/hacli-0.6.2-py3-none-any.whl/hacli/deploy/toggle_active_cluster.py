import typer
from typing_extensions import Annotated

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(
    name="toggle_active_cluster",
    help="切换活动集群",
    short_help="切换活动集群"
)
def toggle_active_cluster(
        release: Annotated[str, typer.Argument(
            help="发布版本号",
            show_default=False,
            metavar="VERSION"
        )]
) -> None:
    """
    切换当前的活动集群。

    此命令用于触发 Azure DevOps 流水线来切换活动集群。
    执行后会将流量从当前活动集群切换到非活动集群。

    Args:
        release: 要切换的版本号，例如 "v1.0.0"

    环境变量:
        DEPLOY_PIPELINES_TOGGLE_ACTIVE_CLUSTER_NAME: 切换流水线名称
        DEPLOY_PIPELINES_TOGGLE_ACTIVE_CLUSTER_PARAMETERS: 切换流水线参数配置

    Examples:
        切换到指定版本的集群：
            $ hacli deploy toggle_active_cluster v1.0.0

    注意:
        - 此操作会影响生产环境的流量分配，请谨慎执行
        - 确保目标版本已经在非活动集群上部署并测试通过
        - 执行前请确保已正确设置所需的环境变量
    """
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_TOGGLE_ACTIVE_CLUSTER_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_TOGGLE_ACTIVE_CLUSTER_PARAMETERS")
