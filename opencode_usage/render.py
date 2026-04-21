from rich.console import Console
from rich.table import Table

from .models import UsageEntry


def print_usage(usage_data: list[UsageEntry]) -> None:
    console = Console()
    table = Table(
        title="[bold cyan]Account Usage Limits[/bold cyan]",
        show_header=True,
        header_style="bold magenta",
    )

    table.add_column("Usage Type", style="dim", width=12)
    table.add_column("Capacity", justify="right")
    table.add_column("Reset Timer", style="green")

    for entry in usage_data:
        color = (
            "red"
            if entry.percentage >= 90
            else "yellow"
            if entry.percentage > 50
            else "green"
        )
        table.add_row(
            entry.usage_type,
            f"[{color}]{entry.percentage}%[/{color}]",
            entry.resets_in,
        )

    console.print(table)
