"""Console script for files_to_folders."""
import sys
import click
from pathlib import Path

import re
import logging
from files_to_folders.logger import logger


@click.command()
@click.argument(
    'input_file_or_folder', 
    nargs=-1,
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=True
    ))
@click.option(
    "--output_folder",
    multiple=False,
    required=False,
    default=Path.cwd(),
    type=click.Path(
        exists=True,
        dir_okay=True,
        file_okay=False
    )
)
@click.option(
    "--regexes",
    multiple=True,
    required=True,
    type=click.STRING
)
@click.option(
    "--log_level",
    multiple=False,
    required=False,
    default="ERROR",
    type=click.Choice(["DEBUG","INFO","WARNING","ERROR","CRITICAL"])
)

def main(input_file_or_folder, output_folder, regexes, log_level):
    #####################################
    # Set basics: logging and constants #
    #####################################
    logger.setLevel(getattr(logging, log_level.upper()))
    
    input_files = []
    for file_or_folder in input_file_or_folder:
        file_or_folder = Path(file_or_folder)
        if file_or_folder.is_dir():
            file_or_folder = [file for file in file_or_folder.rglob("*") if file.is_file()]
        elif file_or_folder.is_file():
            file_or_folder = [file_or_folder]
        else:
            raise TypeError(f"File {file_or_folder} is neither recognized as file nor as folder from pathlib.Path. Please check.")
        input_files.extend(file_or_folder)

    ######################
    # Log cli parameters #
    ######################
    logger.debug(f"[Start] Parameters given via command line:")
    logger.debug(f"Log level set to {log_level=}")
    
    for idx, input_file in enumerate(input_files):
        logger.debug(f"Input file {idx}: {input_file=}")
    
    logger.debug(f"Output folder: {output_folder=}")
    
    for idx, regex in enumerate(regexes):
        logger.debug(f"Regex {idx}: {re.compile(regex).pattern}")
    
    logger.debug(f"[End] Parameters given via command line")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
