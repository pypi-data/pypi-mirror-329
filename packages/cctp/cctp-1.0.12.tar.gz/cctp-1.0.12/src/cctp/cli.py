"""Console script for cctp."""

import os

import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for cctp."""
    os.system(" ".join(["uvx", "cookiecutter", "https://gitee.com/gooker_young/cctp.git"]))


if __name__ == "__main__":
    app()
