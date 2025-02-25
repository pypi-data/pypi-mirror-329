import json
from os import environ
from string import Template

import typer
from azure.devops.connection import Connection
from azure.devops.exceptions import AzureDevOpsServiceError
from azure.devops.v7_0.dashboard import TeamContext, Dashboard, DashboardClient, Widget
from azure.devops.v7_0.git import GitClient
from azure.devops.v7_0.pipelines import PipelinesClient, Pipeline, Run
from msrest.authentication import BasicAuthentication


class AzureDevOpsClient:
    def __init__(self, project):
        self.org_url = environ["ORG_URL"]
        self.personal_access_token = environ["PERSONAL_ACCESS_TOKEN"]
        self.project = project
        self.credentials = BasicAuthentication('', self.personal_access_token)
        self.connection = Connection(base_url=self.org_url, creds=self.credentials)

        self.pipeline_client: PipelinesClient = self.connection.clients.get_pipelines_client()
        self.dashboard_client: DashboardClient = self.connection.clients.get_dashboard_client()
        self.git_client: GitClient = self.connection.clients.get_git_client()

    def trigger_pipeline(self, pipeline_id: int, run_parameters: dict) -> Run:
        return self.pipeline_client.run_pipeline(pipeline_id=pipeline_id,
                                                 project=self.project,
                                                 run_parameters=run_parameters)

    def get_pipeline(self, pipeline_id: int) -> Pipeline:
        return self.pipeline_client.get_pipeline(self.project, pipeline_id=pipeline_id)

    def list_pipelines(self) -> list[Pipeline]:
        return self.pipeline_client.list_pipelines(self.project, top=9999)

    def get_pipeline_by_name(self, pipeline_name: str) -> Pipeline | None:
        pipelines: list[Pipeline] = self.pipeline_client.list_pipelines(self.project, top=9999)
        for pipeline in pipelines:
            if pipeline.name == pipeline_name:
                return pipeline

    def get_dashboard(self, team: str, dashboard_id: str) -> Dashboard:
        team_context = TeamContext(project=self.project, team=team)
        return self.dashboard_client.get_dashboard(team_context, dashboard_id=dashboard_id)

    def get_widget_from_dashboard(self, team: str, dashboard_id: str, widget_id: str) -> Widget:
        team_context = TeamContext(project=self.project, team=team)
        return self.dashboard_client.get_widget(team_context, dashboard_id=dashboard_id, widget_id=widget_id)

    def check_release_branch(self, repository_id: str, release_branch_name: str):
        try:
            self.git_client.get_branch(repository_id=repository_id, name=release_branch_name, project=self.project)
            return True
        except AzureDevOpsServiceError as ex:
            return False


def execute_pipeline(release: str,
                     pipeline_name_env_key: str,
                     pipeline_parameter_env_key: str,
                     project_name_env_key: str = "PROJECT_LOCAL_NAME",
                     project_repo_env_key: str = "PROJECT_LOCAL_REPO", **kwargs):
    kwargs["release"] = release

    client = AzureDevOpsClient(environ[project_name_env_key])

    release_branch_name = release if release == "master" else f"release/{release}-Application-Deployment"
    release_branch_exist: bool = client.check_release_branch(environ[project_repo_env_key], release_branch_name)
    if not release_branch_exist:
        typer.secho(f"Release branch {release_branch_name} does not exist", fg=typer.colors.RED)
        return

    pipeline_name = Template(environ[pipeline_name_env_key]).safe_substitute(**kwargs)
    pipeline = client.get_pipeline_by_name(pipeline_name)

    if not pipeline:
        typer.secho(f"Pipeline {pipeline_name} is not existed", fg=typer.colors.RED)
        return

    pipeline_parameter_template = environ[pipeline_parameter_env_key]
    run_parameters = json.loads(Template(pipeline_parameter_template).safe_substitute(**kwargs))
    confirm = typer.confirm(f"Are you sure to trigger pipeline {pipeline_name}?")
    if not confirm:
        return

    web_url: str = pipeline._links.additional_properties.get("web").get('href')
    typer.launch(web_url)
    client.trigger_pipeline(pipeline_id=pipeline.id, run_parameters=run_parameters)
