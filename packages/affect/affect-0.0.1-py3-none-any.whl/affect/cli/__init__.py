"""Affect CLI."""

import typer

from affect.version import print_version_info_rich

app = typer.Typer()


@app.command()
def version() -> None:
    """Show installed plugins versions."""
    print_version_info_rich()
