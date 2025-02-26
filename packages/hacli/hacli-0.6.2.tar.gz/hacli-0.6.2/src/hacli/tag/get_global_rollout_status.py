import os
import re

import typer
from azure.devops.v7_0.dashboard import Widget
from bs4 import BeautifulSoup
from markdown_it import MarkdownIt
from rich import print

from ..utils.ado import AzureDevOpsClient

app = typer.Typer()


def global_rollout_status_internally() -> dict[str, str]:
    """
    从 Azure DevOps 仪表板获取全局发布状态。

    从指定的仪表板小部件中获取活动集群信息和服务标签信息。
    通过解析 Markdown 内容来提取服务的发布标签。

    Returns:
        dict[str, str]: 服务名称和对应标签的映射字典

    Raises:
        Exception: 当找不到活动集群或服务标签时抛出
    """
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

    if not green_clusters: raise Exception("Active cluster was not found from global rollout status")

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

    if not result_map: raise Exception(f"Tags for active cluster {active_cluster} services were not found")

    return result_map.get(active_cluster)


@app.command(
    name="get_global_rollout_status",
    help="获取全局发布状态信息",
    short_help="获取发布状态"
)
def get_global_rollout_status() -> None:
    """
    获取并显示全局发布状态信息。

    此命令从 Azure DevOps 仪表板获取当前活动集群中所有服务的发布标签信息。

    环境变量:
        PROJECT_GLOBAL_NAME: 全局项目名称
        TAG_TEAM: 团队名称
        TAG_DASHBOARD_ID: 仪表板 ID
        TAG_ACTIVE_CLUSTER_WIDGET_ID: 活动集群小部件 ID
        TAG_SERVICES_TAG_WIDGET_ID: 服务标签小部件 ID

    输出:
        以字典格式显示所有服务的标签信息：
        {
            "SERVICE1": "v1.0.0",
            "SERVICE2": "v1.1.0",
            ...
        }

    Examples:
        获取发布状态：
            $ hacli tag get_global_rollout_status

    注意:
        - 需要正确配置 Azure DevOps 访问凭据
        - 确保所有环境变量已正确设置
    """
    tags = global_rollout_status_internally()
    print("Got tags for services\n")
    print(tags)
