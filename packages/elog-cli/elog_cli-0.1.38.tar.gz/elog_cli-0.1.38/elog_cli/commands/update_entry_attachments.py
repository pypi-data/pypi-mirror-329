import click
from rich.console import Console
from elog_cli.auth_manager import AuthManager  # Import the AuthManager type
from elog_cli.hl_api import ElogAPIError, ElogApi

console = Console()

@click.command()
@click.argument("entry_id", nargs=1)
@click.pass_context
def update_entry_attachments(ctx, entry_id: str):
    """Force the update on all the attachments of an entry."""
    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        elog_api.update_entry_attachments(entry_id)
        console.print("Attachments updated successfully.")
    except ElogAPIError as e:
        raise click.ClickException(e)
