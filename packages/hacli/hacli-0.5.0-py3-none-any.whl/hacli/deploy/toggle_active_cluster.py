import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(name="toggle_active_cluster")
def toggle_active_cluster(release: str):
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_TOGGLE_ACTIVE_CLUSTER_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_TOGGLE_ACTIVE_CLUSTER_PARAMETERS")
