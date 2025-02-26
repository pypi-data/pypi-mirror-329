import rich_click as click

from union.cli._app_common import DeployApplicationGroupForFiles


@click.group(name="deploy")
def deploy():
    """Deploy a resource."""


app_help = """Deploy application on Union."""
app_group = DeployApplicationGroupForFiles(
    name="apps",
    help=app_help,
    command_name="deploy",
)
deploy.add_command(app_group)
