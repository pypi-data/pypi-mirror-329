"""Version information for affect."""

import importlib
import sys

from rich.console import Console
from rich.table import Table

from affect.settings import settings

__version__ = "0.0.2"

plugins: list[str] = []


def print_version_info_rich() -> None:
    """Print affect versions and paths."""
    table = Table(title="Modules")
    table.add_column("Package", justify="right", style="cyan", no_wrap=True)
    table.add_column("version", style="magenta")
    table.add_column("Path", justify="right", style="green")

    table.add_row("python", sys.version, str(sys.executable))
    table.add_row("affect", __version__, str(settings.path.ROOT))

    for plugin in plugins:
        try:
            m = importlib.import_module(plugin)
            try:
                table.add_row(plugin, str(m.__version__), str(m.__path__))
            except AttributeError:
                table.add_row(plugin, "", "")
        except ImportError:
            table.add_row(plugin, "not installed", "")

    console = Console()
    console.print(table)
