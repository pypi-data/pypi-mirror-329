import click
from elog_cli.auth_manager import AuthManager
from elog_cli.hl_api import ElogAPIError, ElogApi

@click.command()
@click.pass_context
def list_logbooks(ctx):
    """List all logbooks."""
    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        logbooks = elog_api.list_logbooks() # Get the authenticated client
        if logbooks is not None:
                print(", ".join(logbook.name for logbook in logbooks))
    except ElogAPIError as e:
        raise click.ClickException(e)
