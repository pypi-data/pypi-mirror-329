import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(name="import_global_external_images")
def import_global_external_images():
    execute_pipeline(release="master",
                     pipeline_name_env_key="DEPLOY_PIPELINES_IMPORT_GLOBAL_EXTERNAL_IMAGES_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_IMPORT_GLOBAL_EXTERNAL_IMAGES_PARAMETERS",
                     project_name_env_key="PROJECT_GLOBAL_NAME",
                     project_repo_env_key="PROJECT_GLOBAL_REPO")
