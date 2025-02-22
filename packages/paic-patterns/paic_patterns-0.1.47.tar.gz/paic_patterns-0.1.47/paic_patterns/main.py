import typer
import webbrowser
import logging
from .modules.logging import setup_logging
from dotenv import load_dotenv
from . import __version__

from .commands import spec_commands, member_commands

load_dotenv()  # Load .env file before other imports

# Initialize logging
setup_logging()


def version_callback(value: bool):
    if value:
        typer.echo("PAIC Patterns Version:")
        typer.echo(__version__)
        raise typer.Exit()


app = typer.Typer(
    name="paic",
    help="Principled AI Coding Patterns for large-scale, max-compute, low-error engineering in the GenAI Age.",
    no_args_is_help=True,
)

app.add_typer(spec_commands.app, name="spec")
app.add_typer(member_commands.app, name="member")


@app.command("docs")
def docs():
    """
    Command Name:
        Open Documentation

    Usage Template:
        paic docs

    Description:
        Open the PAIC Patterns documentation in your default web browser.

    Examples Usage:
        paic docs
    """
    url = "https://agenticengineer.com/principled-ai-coding/member-assets/paic-patterns"
    logging.info("Opening documentation", extra={"rich_type": "text", "value": url})
    webbrowser.open(url)


@app.callback()
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        False,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Show the current version and exit",
    ),
):
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
        raise typer.Exit()


def main():
    app()


if __name__ == "__main__":
    main()
