from typing import Any
import questionary
from rich.table import Table
from rich.console import Console

console = Console()


def handle_visualize(sheet_data: list[dict[str, Any]]):
    if len(sheet_data) > 50:
        confirmed = questionary.confirm(
            message=f"Current sheet has {len(sheet_data)} rows, are you sure you want to visualize in the terminal?",
            default=False,
        ).ask()
        if not confirmed:
            console.print("Okay, bye")
            return

    headers = list(sheet_data[0].keys())
    table = Table(show_header=True, show_lines=True)
    for h in headers:
        table.add_column(h, header_style="bold blue")
    for entry in sheet_data:
        values = [str(v) for v in entry.values()]
        table.add_row(*values)

    console.print(table)
