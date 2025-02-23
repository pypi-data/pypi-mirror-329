import typer

app = typer.Typer()


@app.command()
def deploy(service_name: str, release: str, service_tag: str):
    print(f"Deploying service: {service_name}, {release}, {service_tag}")


@app.command()
def services1(name: str, release: str, tag: str):
    print(f"Deploying service: {name}, {release}, {tag}")