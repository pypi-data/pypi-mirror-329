import typer

from ..utils.ado import execute_pipeline

app = typer.Typer()


@app.command(name="teardown_inactive_cluster")
def teardown_inactive_cluster(release: str):
    execute_pipeline(release=release,
                     pipeline_name_env_key="DEPLOY_PIPELINES_TEARDOWN_INACTIVE_CLUSTER_NAME",
                     pipeline_parameter_env_key="DEPLOY_PIPELINES_TEARDOWN_INACTIVE_CLUSTER_PARAMETERS")
