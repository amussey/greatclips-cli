"""Click CLI for Great Clips API."""

import click

from .store import store
from .customer import customer


@click.group()
def cli():
    """Great Clips CLI - Command line tool for Great Clips API."""
    pass


# Register subcommand groups
cli.add_command(store)
cli.add_command(customer)


if __name__ == '__main__':
    cli()
