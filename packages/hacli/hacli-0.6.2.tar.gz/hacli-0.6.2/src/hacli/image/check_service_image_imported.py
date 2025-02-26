import json
from string import Template

import typer
from azure.containerregistry import ContainerRegistryClient
from azure.core.exceptions import ResourceNotFoundError
from azure.identity import DefaultAzureCredential

from ..tag.get_global_rollout_status import global_rollout_status_internally

app = typer.Typer()

default_services = {
    "pm": "product-management",
    "sm": "service-management",
    "um": "user-management",
    "vm": "vehicle-management",
    "st": "system"
}

import os


def get_service_image_names(parent_dir):
    """
    获取指定目录下包含 'cn' 子目录的所有服务名称。

    Args:
        parent_dir: 父目录路径

    Returns:
        包含 'cn' 子目录的服务名称列表
    """
    directories_with_cn = []
    for subdir, dirs, files in os.walk(parent_dir):
        if 'cn' in dirs:
            directories_with_cn.append(os.path.basename(subdir))
    return directories_with_cn


@app.command(
    name="check_service_image_imported",
    help="检查服务镜像是否已导入到容器注册表",
    short_help="检查服务镜像状态"
)
def check_service_image_imported() -> None:
    """
    检查所有服务的镜像是否已成功导入到 Azure 容器注册表。

    此命令会检查配置中定义的所有服务的镜像是否已经成功导入到容器注册表中。
    检查基于全局发布状态中的标签进行验证。

    环境变量:
        PROJECT_LOCAL_GIT_LOCAL_WORKING_DIR: 项目本地 Git 工作目录
        SERVICES_CONFIGURATION_DIR: 服务配置目录
        SERVICES_DEPLOYMENT_SETTING_DIR_TEMPLATE: 服务部署设置目录模板
        SERVICES_DEPLOYMENT_SETTING_SERVICE_KEY_TEMPLATE: 服务部署设置键模板
        PROJECT_LOCAL_ACR_URL: Azure 容器注册表 URL

    输出:
        - 对于每个服务，如果所有镜像都已导入，显示绿色成功消息
        - 如果有镜像未找到或检查出错，显示红色错误消息

    Examples:
        检查所有服务镜像：
            $ hacli image check_service_image_imported

    注意:
        - 需要 Azure 认证凭据
        - 确保所有必需的环境变量已正确设置
        - 检查基于服务配置文件中定义的服务列表
    """
    rollout_tags: dict[str, str] = global_rollout_status_internally()

    project_dir = os.environ["PROJECT_LOCAL_GIT_LOCAL_WORKING_DIR"]
    service_configuration_parent_dir = os.environ["SERVICES_CONFIGURATION_DIR"]
    service_configuration_setting_template_dir = os.environ["SERVICES_DEPLOYMENT_SETTING_DIR_TEMPLATE"]
    deployment_setting_service_key_template = os.environ["SERVICES_DEPLOYMENT_SETTING_SERVICE_KEY_TEMPLATE"]
    ENDPOINT = os.environ["PROJECT_LOCAL_ACR_URL"]

    credential = DefaultAzureCredential()
    with ContainerRegistryClient(ENDPOINT, credential) as client:
        for key, value in rollout_tags.items():
            service = default_services.get(key.lower())
            service_folder = os.path.join(project_dir, service_configuration_parent_dir, service)
            services_from_configuration = get_service_image_names(service_folder)
            service_configuration_setting_file = os.path.join(project_dir, Template(
                service_configuration_setting_template_dir).safe_substitute(service=service))

            with open(service_configuration_setting_file, "r") as f:
                loads: dict = json.loads(f.read())
                substitute = Template(deployment_setting_service_key_template).safe_substitute(service=service)
                get = loads.get(substitute)
                if get.get("services"):
                    services_from_configuration = [item for item in services_from_configuration if
                                                   item in get.get("services")]
            check_pass = True
            for service_module in services_from_configuration:
                try:
                    client.get_tag_properties(repository=f"service/{service_module}", tag=value)
                except ResourceNotFoundError:
                    check_pass = False
                    typer.secho(f"Service: {service_module}, Tag: '{value}' is not existed!", fg=typer.colors.RED)
                except Exception as e:
                    check_pass = False
                    typer.secho(f"Service: {service_module}, Tag: '{value}' checks with exception", fg=typer.colors.RED)

            if check_pass:
                typer.secho(f"Service: {service}, Tag: '{value}' , all images imported!", fg=typer.colors.GREEN)
