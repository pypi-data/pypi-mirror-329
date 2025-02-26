import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(
    name="import_global_external_images",
    help="导入全局外部镜像到容器注册表",
    short_help="导入外部镜像"
)
def import_global_external_images() -> None:
    """
    从外部源导入全局镜像到 Azure 容器注册表。

    此命令会触发 Azure DevOps 流水线来导入全局外部镜像。
    导入过程基于全局仓库的 master 分支配置进行。

    环境变量:
        DEPLOY_PIPELINES_IMPORT_GLOBAL_EXTERNAL_IMAGES_NAME: 导入流水线名称
        DEPLOY_PIPELINES_IMPORT_GLOBAL_EXTERNAL_IMAGES_PARAMETERS: 导入流水线参数
        PROJECT_GLOBAL_NAME: 全局项目名称
        PROJECT_GLOBAL_REPO: 全局仓库名称

    Examples:
        导入全局外部镜像：
            $ hacli image import_global_external_images

    注意:
        - 确保已正确设置所有必需的环境变量
        - 确保有权限访问全局仓库和目标容器注册表
        - 此操作可能需要较长时间，具体取决于镜像大小和数量
    """
    execute_pipeline(release="master",
                     pipeline_name_env_key="DEPLOY_PIPELINES_IMPORT_GLOBAL_EXTERNAL_IMAGES_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_IMPORT_GLOBAL_EXTERNAL_IMAGES_PARAMETERS",
                     project_name_env_key="PROJECT_GLOBAL_NAME",
                     project_repo_env_key="PROJECT_GLOBAL_REPO")
