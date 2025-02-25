import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(name="sync_global_repo")
def sync_global_repo():
    execute_pipeline(release="master",
                     pipeline_name_env_key="DEPLOY_PIPELINES_SYNC_GLOBAL_REPO_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_SYNC_GLOBAL_REPO_PARAMETERS",
                     project_name_env_key="PROJECT_GLOBAL_NAME",
                     project_repo_env_key="PROJECT_GLOBAL_REPO")
