import click
import os
from elog_cli.auth_manager import AuthManager  # Import the AuthManager type
from elog_cli.hl_api import ElogAPIError, ElogApi
from elog_cli.elog_management_backend_client.types import File
from elog_cli.elog_management_backend_client.models import NewEntryWithAttachmentBody, NewEntryDTO

@click.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.pass_context
def import_entry(ctx, file_path: str):
    """Create a new entry with a title, text, and optional tags."""
    title:str = ""
    text:str = ""
    tags: list[str] = []
    logbooks: list[str] = []
    attachments: list[str] = []

    # open the file and check if the file is json or xml
    with open(file_path, "r") as file:
        lines = file.readlines()
        if file_path.endswith(".xml"):
            import xml.etree.ElementTree as ET
            root = ET.fromstring("".join(lines))
            title = root.find("title").text if root.find("title") is not None else ""
            text = root.find("text").text if root.find("text") is not None else ""
            tags = [tag.text for tag in root.findall("segment")] if root.find("segment") is not None else []
            logbooks = [logbook.text for logbook in root.findall("logbook")] if root.find("logbook") is not None else []
            attachments = [attachment.text for attachment in root.findall("attachment")] if root.find("attachment") is not None else []
        else:
            click.echo(f"Unsupported file format: {file_path}")
            return

    # Sanitize attachments
    base_path = os.path.dirname(file_path)
    sanitized_attachments = [
        os.path.join(base_path, attachment) if not os.path.isabs(attachment) else attachment
        for attachment in attachments
    ]

    elog_api:ElogApi = ctx.obj["elog_api"] # Retrieve shared ElogApi
    auth_manager:AuthManager = ctx.obj["auth_manager"]  # Retrieve shared AuthManager
    elog_api.set_authentication_token(auth_manager.get_access_token())  # Set the authentication token
    try:
        new_entry = NewEntryWithAttachmentBody(
            entry=NewEntryDTO(
                logbooks=logbooks,
                title=title,
                text=text,
                tags=tags
            ),
            files=[
                File(
                    payload=open(attachment, "rb").read(), 
                    file_name=os.path.basename(attachment),  # Extract only the filename
                    mime_type="application/octet-stream"
                )
                for attachment in sanitized_attachments]
        )
        new_entry_id = elog_api.create_entry(new_entry)
        click.echo(
            "New entry created with id: "+
            click.style(f"{new_entry_id}", fg="green")
        )
    except ElogAPIError as e:
        raise click.ClickException(e)