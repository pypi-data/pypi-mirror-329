import click
from rich.console import Console
from elog_cli.auth_manager import AuthManager  # Import the AuthManager type
from elog_cli.hl_api import ElogAPIError, ElogApi
from elog_cli.elog_management_backend_client.models import EntryDTO
from elog_cli.elog_management_backend_client.types import Unset

console = Console()

@click.command()
@click.option("--entry-id", type=str, required=True, help="The id of the entry.")
@click.pass_context
def show_entry(ctx, entry_id: str):
    """Show the full information of the entry."""
    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        print_entry_info(elog_api.get_full_entry(entry_id))
    except ElogAPIError as e:
        raise click.ClickException(e)

def print_entry_info(entry: EntryDTO):
    console.print(f"[bold]ID:[/bold] {entry.id}")
    console.print(f"[bold]Title:[/bold] {entry.title}")
    console.print(f"[bold]Content:[/bold] {entry.text}")
    console.print(f"[bold]Event At:[/bold] {entry.event_at}")
    console.print(f"[bold]Created At:[/bold] {entry.logged_at}")
    console.print(f"[bold]Author:[/bold] {entry.logged_by}")

    if not isinstance(entry.tags, Unset) and len(entry.tags) > 0:
        console.print(f"[bold]Tags:[/bold] {', '.join(tag.name for tag in entry.tags)}")
    if not isinstance(entry.references, Unset) and len(entry.references) > 0:
        console.print(f"[bold]References:[/bold] {', '.join(ref.id for ref in entry.references)}")
    if not isinstance(entry.referenced_by, Unset) and len(entry.referenced_by) > 0:
        console.print(f"[bold]Referenced By:[/bold] {', '.join(ref.id for ref in entry.referenced_by)}")
    if not isinstance(entry.follow_ups, Unset) and len(entry.follow_ups) > 0:
        console.print(f"[bold]Follow Ups:[/bold] {', '.join(fup.id for fup in entry.follow_ups)}")
    if not isinstance(entry.following_up, Unset) and len(entry.following_up) > 0:
        console.print(f"[bold]Following Up:[/bold] {', '.join(fup.id for fup in entry.following_up)}")
    if not isinstance(entry.history, Unset) and len(entry.history) > 0:
        console.print(f"[bold]History:[/bold] {', '.join(hist.id for hist in entry.history)}")
    if not isinstance(entry.superseded_by, Unset):
        console.print(f"[bold]Superseded By:[/bold] {entry.superseded_by.id}")
    if not isinstance(entry.attachments, Unset) and len(entry.attachments) > 0:
        console.print(f"[bold]Attachments:[/bold] {', '.join(att.file_name for att in entry.attachments)}")