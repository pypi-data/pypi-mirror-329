"""Console script for cctp."""

import envoy
import typer
from rich.console import Console

app = typer.Typer()
console = Console()


@app.command()
def main():
    """Console script for cctp."""
    envoy.run("uvx cookiecutter https://gitee.com/gooker_young/cctp.git")


if __name__ == "__main__":
    app()
