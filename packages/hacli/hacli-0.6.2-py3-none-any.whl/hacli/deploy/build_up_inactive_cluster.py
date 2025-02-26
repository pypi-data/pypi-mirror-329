import typer
from typing_extensions import Annotated

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(
    name="build_up_inactive_cluster",
    help="构建非活动集群的部署流水线",
    short_help="构建非活动集群"
)
def build_up_inactive_cluster(
        release: Annotated[str, typer.Argument(
            help="发布版本号",
            show_default=False,
            metavar="VERSION"
        )]
) -> None:
    """
    触发 Azure DevOps 流水线来构建非活动集群。

    此命令将启动指定的 Azure DevOps 流水线，用于构建和部署非活动集群。
    流水线的具体配置通过环境变量指定。

    Args:
        release: 要部署的版本号，例如 "v1.0.0"

    环境变量:
        DEPLOY_PIPELINES_BUILD_UP_INACTIVE_CLUSTER_NAME: 流水线名称
        DEPLOY_PIPELINES_BUILD_UP_INACTIVE_CLUSTER_PARAMETERS: 流水线参数配置

    Examples:
        部署指定版本到非活动集群：
            $ hacli deploy build_up_inactive_cluster v1.0.0

    注意:
        - 执行前请确保已正确设置所需的环境变量
        - 确保指定的版本号在代码仓库中存在
    """
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_BUILD_UP_INACTIVE_CLUSTER_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_BUILD_UP_INACTIVE_CLUSTER_PARAMETERS")
