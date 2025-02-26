import json
import os
import re

import typer
from azure.devops.v7_0.dashboard import Widget
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from rich import print

from ..utils.ado import AzureDevOpsClient

app = typer.Typer()


def global_rollout_status_internally() -> dict[str, str] | None:
    client = AzureDevOpsClient(os.environ["PROJECT_GLOBAL_NAME"])

    tag_team = os.environ["TAG_TEAM"]
    tag_dashboard_id = os.environ["TAG_DASHBOARD_ID"]
    tag_active_cluster_widget_id = os.environ["TAG_ACTIVE_CLUSTER_WIDGET_ID"]
    tag_services_tag_widget_id = os.environ["TAG_SERVICES_TAG_WIDGET_ID"]

    widget: Widget = client.get_widget_from_dashboard(team=tag_team,
                                                      dashboard_id=tag_dashboard_id,
                                                      widget_id=tag_active_cluster_widget_id)
    green_clusters = [
        re.sub(r"[`]", "", match[0].strip())
        for match in re.findall(r"\| (.*?) \| (.*?) \| (.*?) \|", widget.settings)
        if "green" in match[1].lower() and "green" in match[2].lower()
    ]

    if green_clusters:
        active_cluster = green_clusters[0]
        tag_widget: Widget = client.get_widget_from_dashboard(team=tag_team,
                                                              dashboard_id=tag_dashboard_id,
                                                              widget_id=tag_services_tag_widget_id)
        md = MarkdownIt('js-default')
        html_content = md.render(tag_widget.settings)
        soup = BeautifulSoup(html_content, 'html.parser')

        result_map = {}
        for table in soup.find_all('table'):
            cluster_name = table.find('code').text.strip()
            cluster_data = {row.find_all('td')[0].text.strip(): row.find_all('td')[1].text.strip()
                            for row in table.find_all('tr')[1:]}

            result_map[cluster_name] = cluster_data
        return result_map.get(active_cluster)


@app.command(name="get_global_rollout_status.py")
def get_global_rollout_status():
    internally = global_rollout_status_internally()
    if internally:
        print("Got tags for services\n")
        print(json.dumps(internally, indent=2))
    else:
        msg = typer.style("No Active cluster Found", fg=typer.colors.RED, bold=True)
        typer.echo(msg)
