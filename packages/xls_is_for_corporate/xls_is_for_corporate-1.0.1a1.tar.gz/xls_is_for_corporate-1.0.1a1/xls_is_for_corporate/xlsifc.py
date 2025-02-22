from typing import Any, Optional
from click import command, option, version_option
from click.types import Choice, Path
from rich.console import Console
from xls_is_for_corporate.converter import Spreadsheet
from xls_is_for_corporate.table_utils import handle_visualize
import questionary
import json
from csv import DictWriter

console = Console()
CSV_FORMAT = "csv"
JSON_FORMAT = "json"


def save_json(sheet_data: list[dict[str, Any]], file: str):
    with open(file, "w") as json_file:
        json.dump(obj=sheet_data, fp=json_file)


def save_csv(sheet_data: list[dict[str, Any]], file: str):
    with open(file, "w") as csv_file:
        headers = sheet_data[0].keys()
        dictwriter = DictWriter(f=csv_file, fieldnames=headers)
        dictwriter.writeheader()
        dictwriter.writerows(sheet_data)


def handle_save(sheet_data: list[dict[str, Any]], format: str, output: str):
    if not format:
        format = questionary.select(
            message="In which format would you like to save?",
            choices=[JSON_FORMAT, CSV_FORMAT],
        ).ask()

    if not output:
        output = questionary.path(message="Where do you want to save it?").ask()

    if format == JSON_FORMAT:
        save_json(sheet_data, output)
    elif format == CSV_FORMAT:
        save_csv(sheet_data, output)


@command(name="xls is for corporate")
@option(
    "--file",
    "-f",
    type=Path(exists=True, file_okay=True, dir_okay=False, readable=True),
    required=True,
)
@option(
    "--format",
    "-t",
    help="Format to convert into",
    type=Choice([JSON_FORMAT, CSV_FORMAT]),
    required=False,
)
@option("--output", "-o", help="Output file", type=Path(writable=True), required=False)
@option(
    "--sheet",
    "-s",
    help="Speficic sheet inside workbook (if not provided, you will be asked",
    type=str,
    required=False,
)
@version_option()
def cli(file: str, format: str, output: str, sheet: Optional[str]):
    console.log(f"Reading input from file {file}")
    spreadsheet = Spreadsheet(path=file)
    worksheets = spreadsheet.get_worksheets()
    if sheet and sheet in worksheets:
        sheet_data = spreadsheet.read_sheet(sheet=sheet)
    else:
        ws = questionary.select(
            message="Which sheet do you want to convert?", choices=worksheets
        ).ask()
        sheet_data = spreadsheet.read_sheet(sheet=ws)

    should_save = False
    if not should_save:
        should_save = questionary.confirm(
            message="Do you want to save into a file? (Press no if you just want to visualize)",
            default=False,
        ).ask()
    if should_save:
        handle_save(sheet_data, format, output)
        return

    handle_visualize(sheet_data)


if __name__ == "__main__":
    cli()
