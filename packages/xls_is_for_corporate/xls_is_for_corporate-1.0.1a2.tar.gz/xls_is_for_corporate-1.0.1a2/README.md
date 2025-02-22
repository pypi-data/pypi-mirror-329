# XLS/XLSX is for corporate

A (very) simple tool to read a xls/xlsx file and either output
it as a table in the terminal or save it as json or csv into a file

## Usage

```text
Usage: xlsifc [OPTIONS]

Options:
  -f, --file FILE          [required]
  -t, --format [json|csv]  Format to convert into
  -o, --output PATH        Output file
  -s, --sheet TEXT         Speficic sheet inside workbook (if not provided,
                           you will be asked
  --version                Show the version and exit.
  --help                   Show this message and exit.
```

## Installation

### Using pipx

```commandline
pipx install xls_is_for_corporate
```

### Using pip

```commandline
pip3 install xls_is_for_corporate
```
