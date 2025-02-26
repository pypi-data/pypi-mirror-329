import typer
from typing_extensions import Annotated

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(
    name="deploy_inactive_shared_services",
    help="部署共享服务到非活动集群",
    short_help="部署共享服务"
)
def deploy_inactive_shared_services(
        release: Annotated[str, typer.Argument(
            help="发布版本号",
            show_default=False,
            metavar="VERSION"
        )],
        tag: Annotated[str, typer.Argument(
            help="部署标签",
            show_default=False,
            metavar="TAG"
        )]
) -> None:
    """
    将共享服务部署到非活动集群。

    此命令用于将共享服务部署到非活动集群中。部署时需要指定版本号和标签。

    Args:
        release: 要部署的版本号，例如 "v1.0.0"
        tag: 部署使用的标签，用于标识部署目标

    环境变量:
        DEPLOY_PIPELINES_DEPLOY_INACTIVE_SHARED_SERVICES_NAME: 部署流水线名称
        DEPLOY_PIPELINES_DEPLOY_INACTIVE_SHARED_SERVICES_PARAMETERS: 部署流水线参数配置

    Examples:
        部署指定版本的共享服务：
            $ hacli deploy deploy_inactive_shared_services v1.0.0 prod-tag

    注意:
        - 确保提供的版本号在代码仓库中存在
        - 确保标签与目标环境匹配
        - 执行前请确保已正确设置所需的环境变量
    """
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_DEPLOY_INACTIVE_SHARED_SERVICES_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_DEPLOY_INACTIVE_SHARED_SERVICES_PARAMETERS",
                     tag=tag)
