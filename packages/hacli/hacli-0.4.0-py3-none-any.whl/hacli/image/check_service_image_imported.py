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
    directories_with_cn = []
    for subdir, dirs, files in os.walk(parent_dir):
        if 'cn' in dirs:
            directories_with_cn.append(os.path.basename(subdir))
    return directories_with_cn


@app.command(name="check_service_image_imported")
def check_service_image_imported():
    rollout_tags: dict[str, str] | None = global_rollout_status_internally()
    if rollout_tags is None:
        typer.secho("Global rollout status is None", fg=typer.colors.RED)
        return

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
