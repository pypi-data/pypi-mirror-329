import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(
    name="purge_local_images",
    help="清理本地容器注册表中的镜像",
    short_help="清理本地镜像"
)
def purge_local_images() -> None:
    """
    清理本地容器注册表中的旧镜像。

    此命令会触发 Azure DevOps 流水线来清理本地容器注册表中的旧镜像。
    清理操作基于预设的策略进行，通常会保留最新的几个版本。

    环境变量:
        DEPLOY_PIPELINES_PURGE_LOCAL_IMAGES_NAME: 清理流水线名称
        DEPLOY_PIPELINES_PURGE_LOCAL_IMAGES_PARAMETERS: 清理流水线参数配置

    Examples:
        清理本地镜像：
            $ hacli image purge_local_images

    注意:
        - 此操作不可逆，请确保要清理的镜像确实不再需要
        - 确保已正确设置所需的环境变量
        - 清理过程可能需要一些时间，具体取决于镜像数量
    """
    execute_pipeline(
        release="master",
        pipeline_name_env_key="DEPLOY_PIPELINES_PURGE_LOCAL_IMAGES_NAME",
        pipeline_parameter_env_key="DEPLOY_PIPELINES_PURGE_LOCAL_IMAGES_PARAMETERS"
    )
