import json
import os
from string import Template

import typer
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from rich import print

from ..tag.get_global_rollout_status import global_rollout_status_internally

app = typer.Typer()

tag_product_services = {
    "pm": "product-management",
    "sm": "service-management",
    "um": "user-management",
    "vm": "vehicle-management",
    "st": "system"
}


@app.command(
    name="check_services_deployment_status",
    help="检查服务在活动集群中的部署状态",
    short_help="检查服务部署状态"
)
def check_services_deployment_status() -> None:
    """
    检查所有服务在活动集群中的部署状态。

    此命令会检查所有服务在当前活动集群中的部署状态，通过比对 Key Vault 中存储的
    部署标签与全局发布状态中的标签来确定服务是否已更新到最新版本。

    环境变量:
        PROJECT_LOCAL_KEY_VAULT_URL: Azure Key Vault URL
        PROJECT_LOCAL_ACTIVE_CLUSTER_KEY_VAULT_KEY: 活动集群的 Key Vault 键名
        PROJECT_LOCAL_PRODUCT_DEPLOYED_KEY_VAULT_KEY: 产品部署标签的 Key Vault 键名模板

    输出:
        JSON 格式的部署状态报告，包含每个服务的状态：
        {
            "product-management": true,
            "service-management": true,
            ...
        }
        true 表示服务已更新到最新版本，false 表示需要更新

    Examples:
        检查所有服务的部署状态：
            $ hacli image check_services_deployment_status

    注意:
        - 需要 Azure 认证凭据
        - 确保所有必需的环境变量已正确设置
        - 确保有权限访问 Key Vault
    """
    rollout_tags: dict[str, str] = global_rollout_status_internally()

    key_vault_uri = os.environ["PROJECT_LOCAL_KEY_VAULT_URL"]

    credential = DefaultAzureCredential()
    client = SecretClient(vault_url=key_vault_uri, credential=credential)
    active_cluster_key = os.environ["PROJECT_LOCAL_ACTIVE_CLUSTER_KEY_VAULT_KEY"]
    active_cluster = client.get_secret(active_cluster_key).value

    res = {}
    for key, value in rollout_tags.items():
        product = tag_product_services.get(key.lower())
        product_tag_key = Template(os.environ["PROJECT_LOCAL_PRODUCT_DEPLOYED_KEY_VAULT_KEY"]).safe_substitute(
            active_cluster=active_cluster, product=product)
        tag = client.get_secret(product_tag_key).value
        res[product] = value == tag

    print(json.dumps(res, indent=2))
