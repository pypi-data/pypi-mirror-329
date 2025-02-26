import typer

from . import (
    build_up_inactive_cluster,
    deploy_inactive_services,
    deploy_inactive_shared_services,
    sync_global_repo,
    teardown_inactive_cluster,
    toggle_active_cluster,
    update_active_service_config
)

app = typer.Typer()

app.add_typer(build_up_inactive_cluster.app)
app.add_typer(deploy_inactive_services.app)
app.add_typer(deploy_inactive_shared_services.app)
app.add_typer(sync_global_repo.app)
app.add_typer(teardown_inactive_cluster.app)
app.add_typer(toggle_active_cluster.app)
app.add_typer(update_active_service_config.app)
