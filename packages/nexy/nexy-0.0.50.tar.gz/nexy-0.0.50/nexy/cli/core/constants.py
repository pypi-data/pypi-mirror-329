"""
Author: Espoir Loém

This module defines the core constants used across the Nexy CLI.
"""

from rich.console import Console
from typer import Typer

# Initialize the console for rich text output
console = Console()

# Initialize the Typer application with a help message
cmd = Typer(help="Nexy CLI - Framework de développement web moderne pour Python")


