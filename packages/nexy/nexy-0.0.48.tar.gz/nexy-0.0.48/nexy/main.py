
from typer import Option
from nexy.cli.core.constants import CMD,Console
from nexy.cli.commands import add, generate,new,info,serve,dev


@CMD.command()
def version(
    version: bool = Option(False, "--version", help="Show the version of Nexy CLI")
):
    """Displays the version of Nexy CLI."""
    if version:
        Console.print("[green]Nexy CLI version 1.0.0[/green]")


def app():
    CMD()

