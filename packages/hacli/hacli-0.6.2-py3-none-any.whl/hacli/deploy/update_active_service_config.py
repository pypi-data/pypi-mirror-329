import typer
from typing_extensions import Annotated

from ..utils.ado import execute_pipeline

app = typer.Typer()

service_name_abbr_list = [
    "pm",
    "sm",
    "um",
    "vm",
    "shared",  # TODO..
]


@app.command(
    name="update_active_service_config",
    help="更新活动集群中服务的配置",
    short_help="更新服务配置"
)
def update_active_service_config(
        release: Annotated[str, typer.Argument(
            help="发布版本号",
            show_default=False,
            metavar="VERSION"
        )],
        product: Annotated[str, typer.Argument(
            help="产品名称",
            show_default=False,
            metavar="PRODUCT"
        )],
        service: Annotated[str, typer.Argument(
            help="服务名称",
            show_default=False,
            metavar="SERVICE"
        )]
) -> None:
    """
    更新活动集群中指定服务的配置。

    此命令用于触发 Azure DevOps 流水线来更新活动集群中特定服务的配置。
    可以针对不同的产品和服务进行配置更新。

    Args:
        release: 要更新的版本号，例如 "v1.0.0"
        product: 产品名称，将自动转换为大写
        service: 服务名称，支持的值: pm, sm, um, vm, shared

    环境变量:
        DEPLOY_PIPELINES_UPDATE_ACTIVE_SERVICE_CONFIG_NAME: 更新配置流水线名称
        DEPLOY_PIPELINES_UPDATE_ACTIVE_SERVICE_CONFIG_PARAMETERS: 更新配置流水线参数

    Examples:
        更新产品管理服务配置：
            $ hacli deploy update_active_service_config v1.0.0 product pm

        更新共享服务配置：
            $ hacli deploy update_active_service_config v1.0.0 shared shared

    注意:
        - 确保提供的服务名称在支持列表中
        - 确保目标版本存在对应的配置文件
        - 执行前请确保已正确设置所需的环境变量
    """
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_UPDATE_ACTIVE_SERVICE_CONFIG_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_UPDATE_ACTIVE_SERVICE_CONFIG_PARAMETERS",
                     product=product.upper(),
                     service=service)
