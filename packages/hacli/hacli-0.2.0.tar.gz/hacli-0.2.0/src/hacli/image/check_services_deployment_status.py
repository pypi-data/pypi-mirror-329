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


@app.command(name="check_services_deployment_status")
def check_services_deployment_status():
    rollout_tags: dict[str, str] | None = global_rollout_status_internally()
    if rollout_tags is None:
        typer.echo("Global rollout status is None")
        return

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
