"""Command to display the current RoyalFlush version."""

import click

from royalflush import __version__


@click.command(name="version")
@click.pass_context
def version_cmd(_: click.Context) -> None:
    """
    Show the current version of RoyalFlush.

    Usage:
        royalflush version
    """
    click.echo(f"Royal FLush version: {__version__}")
