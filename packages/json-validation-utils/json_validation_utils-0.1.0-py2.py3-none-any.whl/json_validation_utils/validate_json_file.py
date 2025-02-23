"""Validate a JSON file using the JSON schema file."""

import click
import json
import jsonschema
from jsonschema import validate
import logging
import os
import pathlib
import sys

from rich.console import Console
from datetime import datetime

from json_validation_utils import constants
from json_validation_utils.file_utils import (
    check_infile_status,
    get_file_size,
    get_line_count,
    calculate_md5,
)


DEFAULT_OUTDIR = os.path.join(
    constants.DEFAULT_OUTDIR_BASE,
    os.path.splitext(os.path.basename(__file__))[0],
    constants.DEFAULT_TIMESTAMP,
)

error_console = Console(stderr=True, style="bold red")

console = Console()


def validate_verbose(ctx, param, value):
    """Validate the validate option.

    Args:
        ctx (Context): The click context.
        param (str): The parameter.
        value (bool): The value.

    Returns:
        bool: The value.
    """

    if value is None:
        click.secho(
            "--verbose was not specified and therefore was set to 'True'", fg="yellow"
        )
        return constants.DEFAULT_VERBOSE
    return value


@click.command()
@click.option("--infile", help="The JSON file to be validated.")
@click.option("--logfile", help="The log file.")
@click.option(
    "--outdir",
    help=f"The default is the current working directory - default is '{DEFAULT_OUTDIR}'.",
)
@click.option("--outfile", help="The validation report output file.")
@click.option("--schema_file", help="The JSON schema file.")
@click.option(
    "--verbose",
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{constants.DEFAULT_VERBOSE}'.",
    callback=validate_verbose,
)
def main(
    infile: str,
    logfile: str,
    outdir: str,
    outfile: str,
    schema_file: str,
    verbose: bool,
):
    """Validate a JSON file using the JSON schema file."""

    error_ctr = 0

    if infile is None:
        error_console.print("--infile was not specified")
        error_ctr += 1

    if schema_file is None:
        error_console.print("--schema_file was not specified")
        error_ctr += 1

    if error_ctr > 0:
        click.echo(click.get_current_context().get_help())
        sys.exit(1)

    check_infile_status(infile, "json")

    check_infile_status(schema_file, "json")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(
            f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]"
        )

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)
        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if outfile is None:
        outfile = os.path.join(outdir, "json_validation_report.txt")
        console.print(
            f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]"
        )

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        console.print(
            f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]"
        )

    logging.basicConfig(
        filename=logfile,
        format=constants.DEFAULT_LOGGING_FORMAT,
        level=constants.DEFAULT_LOGGING_LEVEL,
    )

    # Load the schema
    with open(schema_file, "r") as sf:
        schema = json.load(sf)

    # Load the JSON file you want to validate
    with open(infile, "r") as jf:
        data = json.load(jf)

    # Validate the JSON data against the schema
    is_valid = False
    try:
        validate(instance=data, schema=schema)
        logging.info("The JSON file is valid.")
        is_valid = True
    except jsonschema.exceptions.ValidationError as ve:
        print(f"Validation error: {ve.message}")

    ## Generate a report file
    with open(outfile, "w") as of:
        of.write(f"## method-created: {os.path.abspath(__file__)}\n")
        of.write(
            f"## date-created: {str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))}\n"
        )
        of.write(f"## created-by: {os.environ.get('USER')}\n")
        of.write(f"## JSON infile: {infile}\n")
        of.write(f"## JSON schema file: {schema_file}\n")
        of.write(f"## logfile: {logfile}\n")
        of.write(f"## validation-status: {is_valid}\n")

        of.write(f"## file-size: {get_file_size(infile)}\n")
        of.write(f"## line-count: {get_line_count(infile)}\n")
        of.write(f"## md5checksum: {calculate_md5(infile)}\n")

        if is_valid:
            of.write(f"The JSON file is valid.\n")
        else:
            of.write(f"The JSON file is invalid.\n")

    print(f"Wrote validation report file '{outfile}'")

    if verbose:
        print(f"The log file is '{logfile}'")
        console.print(
            f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]"
        )


if __name__ == "__main__":
    main()
