import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(name="deploy_inactive_shared_services")
def deploy_inactive_shared_services(release: str, tag: str):
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_DEPLOY_INACTIVE_SHARED_SERVICES_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_DEPLOY_INACTIVE_SHARED_SERVICES_PARAMETERS",
                     tag=tag)
