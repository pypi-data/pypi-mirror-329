import click

from . import flow, lib
from .setup import check_setup_status, CheckSetupStatusOptions, apply_setup_changes

@click.group()
def cli():
    """
    CLI for Cocoindex.
    """

@cli.command()
def ls():
    """
    List all available flows.
    """
    for name in flow.flow_names():
        click.echo(name)

@cli.command()
@click.argument("flow_name", type=str, required=False)
def show(flow_name: str | None):
    """
    Show the flow spec.
    """
    click.echo(str(_flow_by_name(flow_name)))

@cli.command()
@click.option(
    "-D", "--delete_legacy_flows", is_flag=True, show_default=True, default=False,
    help="Also check / delete flows existing before but no longer exist.")
def setup(delete_legacy_flows):
    """
    Check and apply setup changes.
    """
    options = CheckSetupStatusOptions(delete_legacy_flows=delete_legacy_flows)
    status_check = check_setup_status(options)
    print(status_check)
    if status_check.is_up_to_date():
        return
    if not click.confirm(
        "Changes need to be pushed. Continue? [yes/N]", default=False, show_default=False):
        return
    apply_setup_changes(status_check)

@cli.command()
@click.argument("flow_name", type=str, required=False)
def update(flow_name: str | None):
    """
    Update the index for the flow.
    """
    stats = _flow_by_name(flow_name).update()
    print(stats)

_default_server_settings = lib.ServerSettings.from_env()

@cli.command()
@click.option(
    "-a", "--address", type=str, default=_default_server_settings.address,
    help="The address to bind the server to.")
@click.option(
    "-c", "--cors-origin", type=str, default=_default_server_settings.cors_origin,
    help="The origin of the client (e.g. CocoInsight UI) to allow CORS from.")
def server(address: str, cors_origin: str | None):
    """
    Start a HTTP server providing REST APIs.
    """
    lib.start_server(lib.ServerSettings(address=address, cors_origin=cors_origin))
    input("Press Enter to stop...")


def _flow_name(name: str | None) -> str:
    names = flow.flow_names()
    if name is not None:
        if name not in names:
            raise click.BadParameter(f"Flow {name} not found")
        return name
    if len(names) == 0:
        raise click.UsageError("No flows available")
    elif len(names) == 1:
        return names[0]
    else:
        raise click.UsageError("Multiple flows available, please specify --name")

def _flow_by_name(name: str | None) -> flow.Flow:
    return flow.flow_by_name(_flow_name(name))
