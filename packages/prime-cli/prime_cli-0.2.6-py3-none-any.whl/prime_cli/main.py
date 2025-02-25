import typer

from .commands.availability import app as availability_app
from .commands.config import app as config_app
from .commands.pods import app as pods_app

app = typer.Typer(name="prime", help="Prime Intellect CLI")

app.add_typer(availability_app, name="availability")
app.add_typer(config_app, name="config")
app.add_typer(pods_app, name="pods")


@app.callback(invoke_without_command=True)
def callback(ctx: typer.Context) -> None:
    """Prime Intellect CLI"""
    if ctx.invoked_subcommand is None:
        ctx.get_help()


def run() -> None:
    """Entry point for the CLI"""
    app()
