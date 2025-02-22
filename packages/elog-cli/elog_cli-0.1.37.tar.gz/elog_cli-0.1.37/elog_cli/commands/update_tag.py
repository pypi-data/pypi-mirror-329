import click
from elog_cli.auth_manager import AuthManager
from elog_cli.hl_api import ElogAPIError, ElogApi
from elog_cli.elog_management_backend_client.types import Unset
from elog_cli.elog_management_backend_client.models import LogbookDTO, TagDTO, UpdateTagDTO

@click.command()
@click.pass_context
def update_tag(ctx):
    """List all logbooks permitting to select one, and on that logbook, permit to update a single tag."""
    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        all_logbook_result: list[LogbookDTO] = elog_api.list_logbooks()
        selected_logbook = logbook_selection(all_logbook_result)
        if selected_logbook is None:
            click.echo("No logbook selected.")
            return
        selected_tag = tag_selection(selected_logbook)
        if selected_tag is None:
            click.echo("No tag selected or found.")
            return
        # update tag
        new_tag_dto = update_tag_info(elog_api, selected_tag)
        click.echo(f"Tag updated successfully: {new_tag_dto}")
    except ElogAPIError as e:
        raise click.ClickException(e)


def logbook_selection(logbooks: list[LogbookDTO]) -> LogbookDTO:
    """List all logbooks and select one."""
    if len(logbooks) == 0:
        click.echo("No logbooks found.")
        return None

    click.echo("Select a logbook:")
    for i, logbook in enumerate(logbooks):
        click.echo(f"{i + 1}. {logbook.name}")

    choice = click.prompt("Enter the number of the logbook", type=int)
    if 1 <= choice <= len(logbooks):
        selected_logbook = logbooks[choice - 1]
        click.echo(f"You selected: {selected_logbook.name}")
        return selected_logbook
    else:
        click.echo("Invalid choice. Please try again.")

def tag_selection(logbook: LogbookDTO) -> TagDTO:
    """List all tags and select one."""
    if not isinstance(logbook.tags, Unset) and len(logbook.tags) == 0:
        return None

    click.echo("Select a tag:")
    for i, tag in enumerate(logbook.tags):
        click.echo(f"{i + 1}. {tag.name}")

    choice = click.prompt("Enter the number of the tag", type=int)
    if 1 <= choice <= len(logbook.tags):
        selected_tag = logbook.tags[choice - 1]
        click.echo(f"You selected: {selected_tag.name}")
        return selected_tag
    else:
        return None

def update_tag_info(elog_api:ElogApi, tag: TagDTO)->str:
    """Update the tag information."""
    click.echo(f"Current tag name: {tag.name}")
    click.echo(f"Current tag description: {tag.description}")

    new_name = click.prompt("Enter new tag name", default=tag.name)
    new_description = click.prompt("Enter new tag description", default=tag.description)

    return elog_api.update_tag(tag.logbook.id, tag.id, UpdateTagDTO(name=new_name, description=new_description))

