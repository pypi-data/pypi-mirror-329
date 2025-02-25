import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()

service_name_abbr_list = [
    "pm",
    "sm",
    "um",
    "vm",
    "shared",  # TODO..
]


@app.command(name="update_active_service_config")
def update_active_service_config(release: str, product: str, service: str):
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_UPDATE_ACTIVE_SERVICE_CONFIG_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_UPDATE_ACTIVE_SERVICE_CONFIG_PARAMETERS",
                     product=product.upper(),
                     service=service)
