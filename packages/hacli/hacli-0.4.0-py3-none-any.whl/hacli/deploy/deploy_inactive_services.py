from typing import Optional, List

import typer
from typing_extensions import Annotated

from ..tag.get_global_rollout_status import global_rollout_status_internally
from ..utils.ado import execute_pipeline

app = typer.Typer()

product_tag_mappings = {
    "pm": "pm",
    "sm": "sm",
    "um": "um",
    "vm": "vm",
    "sys": "st"
}


@app.command(name="deploy_inactive_services")
def deploy_inactive_services(release: str,
                             product_names: Annotated[Optional[List[str]], typer.Option("--product")] = None,
                             deploy_all_product: Annotated[bool, typer.Option("--all-product")] = False):
    tags_to_deploy: dict[str, str] | None = global_rollout_status_internally()
    if not tags_to_deploy:
        typer.echo("No tags found from global services deployment")
        return

    if not deploy_all_product and not product_names:
        typer.secho(f"Either specify product name or specify deploy all products.", fg=typer.colors.RED)
        return

    deploy_product = product_names if not deploy_all_product else list(product_tag_mappings.keys())
    valid_deploy_product = {product for product in deploy_product if product in product_tag_mappings}

    for product in valid_deploy_product:
        product_name = product.upper()
        tag = tags_to_deploy[product_tag_mappings[product.lower()].upper()]
        execute_pipeline(release=release,
                         pipeline_name_env_key="DEPLOY_PIPELINES_DEPLOY_INACTIVE_SERVICES_NAME",
                         pipeline_parameter_env_key="DEPLOY_PIPELINES_DEPLOY_INACTIVE_SERVICES_PARAMETERS",
                         product=product_name, tag=tag)
