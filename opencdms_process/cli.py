"""Console script for opencdms_process."""
import sys

import click


@click.command()
def main(args=None):
    """Console script for opencdms_process."""
    # See click documentation at https://click.palletsprojects.com/
    click.echo(
        "Replace this message by putting your code into"
        " opencdms_process.cli.main"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
