import click

from rich.console import Console
from elog_cli.auth_manager import AuthManager  # Import the AuthManager type
from elog_cli.hl_api import ElogAPIError, ElogApi

from elog_cli.elog_management_backend_client.models import  LogbookDTO, ShiftDTO, TagDTO, DetailsAuthorizationDTO
from elog_cli.elog_management_backend_client.models.details_authorization_dto_permission import DetailsAuthorizationDTOPermission
from elog_cli.elog_management_backend_client.types import  Unset

console = Console()

@click.command()
@click.argument("logbooks", nargs=-1)
@click.pass_context
def show_logbook(ctx, logbooks):
    """Show the full information of the logbook identified by LOGBOOKS"""
    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    shown = 0
    try:
        all_logbook_result = elog_api.list_logbooks()
        for log in all_logbook_result:
            if log.name in logbooks:
                shown += 1
                # Fetch the full logbook information using the id
                full_logbook_result: LogbookDTO = elog_api.get_full_logbook(log.id)
                print_logbook_info(full_logbook_result)
                print_separator()
                if shown == len(logbooks):
                    break
    except ElogAPIError as e:
        raise click.ClickException(e)

def print_separator():
    console.print("\n---------------------\n")

def print_logbook_info(log: LogbookDTO):
    console.print(f"[bold]Name:[/bold] {log.name}")
    console.print(f"[bold]ID:[/bold] {log.id}")
    console.print(f"[bold]Read All:[/bold] {log.read_all}")
    console.print(f"[bold]Write All:[/bold] {log.write_all}")

    print_shifts(log.shifts)
    print_tags(log.tags)
    print_authorizations(log.authorizations)

def print_shifts(shifts: list[ShiftDTO]):
    console.print("[bold]Shifts:[/bold]")
    for shift in shifts:
        console.print(f"Name: [bold blue]{shift.name}[/bold blue], Start: {shift.from_}, End: {shift.to}")

def print_tags(tags: list[TagDTO]):
    console.print("[bold]Tags:[/bold]")
    for tag in tags:
        description = tag.description if not isinstance(tag.description, Unset) else "No description"
        console.print(f"Name: [bold blue]{tag.name}[/bold blue], Description: {description}")

def print_authorizations(auth: list[DetailsAuthorizationDTO]):
    console.print("[bold]Authorizations:[/bold]")
    for authorization in auth:
        console.print(f"User: [bold blue]{authorization.owner_name}[/bold blue], User Type: {authorization.owner_type}, Resource: {colorize_permission(authorization.permission)}")

def colorize_permission(permission: DetailsAuthorizationDTOPermission) -> str:
    if permission == DetailsAuthorizationDTOPermission.WRITE:
        color = "red"
    elif permission == DetailsAuthorizationDTOPermission.READ:
        color = "green"
    elif permission == DetailsAuthorizationDTOPermission.ADMIN:
        color = "magenta"
    else:
        color = "grey"
    return f"[{color}]{permission}[/{color}]"