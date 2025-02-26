"""Console script for cctp."""

import os

import typer
from rich.console import Console

from cctp import __version__

app = typer.Typer()
console = Console()


@app.command()
def main(
    version: bool = typer.Option(None, "--version", "-V", help="Show app version and exit."),
):
    """Console script for cctp."""
    if version:
        console.print(f"cctp v{__version__}")
        return

    os.system(" ".join(["uvx", "cookiecutter", "https://gitee.com/gooker_young/cctp.git"]))


if __name__ == "__main__":
    app()
