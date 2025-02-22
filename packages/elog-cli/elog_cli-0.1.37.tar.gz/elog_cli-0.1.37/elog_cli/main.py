import sys
import os
import click
import logging

# Add project root to sys.path for imports (useful for local development)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from elog_cli.hl_api import ElogApi
from elog_cli.auth_manager import AuthManager
from elog_cli.commands.login import login
from elog_cli.commands.create_entry import create_entry
from elog_cli.commands.list_logbooks import list_logbooks
from elog_cli.commands.show_logbook import show_logbook
from elog_cli.commands.show_entry import show_entry
from elog_cli.commands.update_entry_attachments import update_entry_attachments
from elog_cli.commands.import_entry import import_entry
from elog_cli.commands.update_tag import update_tag
from elog_cli.commands.create_tag import create_tag
from elog_cli.commands.list_entries import list_entries

@click.group()
@click.option(
    "--log-level",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"], case_sensitive=False),
    default="ERROR",
    help="Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).",
    show_default=True,
)
@click.option('--production', '-p',type=bool, default=False, is_flag=True, help='Use the production environment specified by $ELOG_CLI_PROD_ENPOINT_URL environment variable.')
@click.pass_context
def cli(ctx, log_level:str, production:bool):
    """
    CLI for Elog Management.
    doc: https://confluence.slac.stanford.edu/display/EEDWAD/CLI+Terminal+Applcation
    """
    ctx.ensure_object(dict)
    auth_namanger = AuthManager()
    auth_namanger.set_environment(production)
    ctx.obj["auth_manager"] = auth_namanger
    ctx.obj["elog_api"] = ElogApi(auth_namanger.get_environment_endpoint())
    logging.basicConfig(
        level=log_level.upper(),
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
try:
    import importlib.metadata
    version = importlib.metadata.version("elog_cli")
    cli = click.version_option(version, prog_name="ELOG CLI", message="%(prog)s Version: %(version)s")(cli)
except ImportError:
    pass

@cli.command()
@click.pass_context
def completion(ctx):
    """Generate shell completion script."""
    shell = os.environ.get("_ELOG_CLI_COMPLETE", "bash_source")
    if shell == "bash_source":
        click.echo("eval \"$(_ELOG_CLI_COMPLETE=bash_source elog-cli)\"")
    elif shell == "zsh_source":
        click.echo("eval \"$(_ELOG_CLI_COMPLETE=zsh_source elog-cli)\"")
    elif shell == "fish_source":
        click.echo("eval (env _ELOG_CLI_COMPLETE=fish_source elog-cli)")
    else:
        click.echo("Unsupported shell for completion setup.")

# Register all commands
cli.add_command(login)
cli.add_command(show_logbook)
cli.add_command(create_entry)
cli.add_command(list_entries)
cli.add_command(list_logbooks)
cli.add_command(show_entry)
cli.add_command(update_entry_attachments)
cli.add_command(import_entry)
cli.add_command(update_tag)
cli.add_command(create_tag)

if __name__ == "__main__":
    cli()