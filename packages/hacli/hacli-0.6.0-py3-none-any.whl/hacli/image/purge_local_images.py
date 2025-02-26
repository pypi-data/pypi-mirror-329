import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(name="purge_local_images")
def purge_local_images():
    execute_pipeline(release="master",
                     pipeline_name_env_key="DEPLOY_PIPELINES_PURGE_LOCAL_IMAGES_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_PURGE_LOCAL_IMAGES_PARAMETERS")
