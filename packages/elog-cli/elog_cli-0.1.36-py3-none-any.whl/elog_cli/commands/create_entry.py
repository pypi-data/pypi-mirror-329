import click
from elog_cli.auth_manager import AuthManager
from elog_cli.hl_api import ElogAPIError, ElogApi
from elog_cli.elog_management_backend_client.models import NewEntryDTO

@click.command()
@click.option("--title", type=str, required=True, help="The title of the entry.")
@click.option("--text", type=str, required=False, help="Optional text for the entry.")
@click.option("--logbooks", multiple=True, type=str, required=True, help="The logbook to add the entry to.")
@click.option("--tags", multiple=True, type=str, required=False, help="Optional tags for the entry.")
@click.option("--attachments",multiple=True, type=str, required=False, help="Optional attachment for the entry.")
@click.option("--supersede-of", type=str, required=False, help="This new entry will be the suersede of the entry with the given id.")
@click.pass_context
def create_entry(ctx, title:str, logbooks:list[str], text:str = None, tags:list[str] = None, attachments:list[str] = None, supersede_of:str = None):
    """Create a new entry with a title, text, and optional tags."""
    tags = [tag for tag in tags if tag]  # Remove empty items
    logbooks = [logbook for logbook in logbooks if logbook]  # Remove empty items
    attachments = [attachment for attachment in attachments if attachment]  # Remove empty items

    click.echo(f"title: {title}")
    click.echo(f"text: {text}")
    click.echo(f"tags: {tags}")  # Now tags is explicitly a list

    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        new_entry_id = elog_api.create_entry(
            NewEntryDTO(
                logbooks=logbooks,
                title=title,
                text=text,
                tags=tags,
                supersede_of=supersede_of
            ), 
            attachments = attachments if attachments is not None else []
            )
        click.echo(
            "New entry created with id: "+
            click.style(f"{new_entry_id}", fg="green")
        )
    except ElogAPIError as e:
        raise click.ClickException(e)