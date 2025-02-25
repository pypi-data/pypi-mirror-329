import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(name="build_up_inactive_cluster")
def build_up_inactive_cluster(release: str):
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_BUILD_UP_INACTIVE_CLUSTER_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_BUILD_UP_INACTIVE_CLUSTER_PARAMETERS")
