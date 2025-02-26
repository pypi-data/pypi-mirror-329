import typer
from rich import print

from ..tag.get_global_rollout_status import global_rollout_status_internally
from ..utils.ado import execute_pipeline

app = typer.Typer()

tag_product_services = {
    "pm": "product-management",
    "sm": "service-management",
    "um": "user-management",
    "vm": "vehicle-management",
    "st": "system",
    "shared": "shared"
}


@app.command(name="import_global_service_images")
def import_global_service_images():
    confirm = typer.confirm("""Are you sure to trigger pipeline to import service images, 
     have you checked service images imported?""")
    if not confirm:
        return

    rollout_tags: dict[str, str] | None = global_rollout_status_internally()
    if rollout_tags is None:
        typer.secho("Global rollout status is None", fg=typer.colors.RED)
        return

    res = {}
    for key, value in tag_product_services.items():
        tag = rollout_tags.get(key.upper(), None)
        if tag:
            execute_pipeline(release="master",
                             pipeline_name_env_key="DEPLOY_PIPELINES_IMPORT_GLOBAL_SERVICE_IMAGES_NAME",
                             pipeline_parameter_env_key="DEPLOY_PIPELINES_IMPORT_GLOBAL_SERVICE_IMAGES_PARAMETERS",
                             project_name_env_key="PROJECT_GLOBAL_NAME",
                             project_repo_env_key="PROJECT_GLOBAL_REPO", product=value, tag=tag)
            res[value] = f"Trigger pipeline to import global service images for {tag}"
        else:
            res[value] = f"Not tag found for product {value}"

    print(res)
