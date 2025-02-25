"""Command Line Interface (CLI) entry point for the Royal FLush package."""

import sys

import click

from royalflush._commands.analyze_logs import analyze_logs_cmd
from royalflush._commands.create_template import create_template_cmd
from royalflush._commands.run import run_cmd
from royalflush._commands.version import version_cmd


def create_cli() -> click.Group:
    """
    Factory function to create the Royal FLush CLI.

    Returns:
        click.Group: The CLI group with all subcommands attached.
    """

    @click.group()
    @click.option("--verbose", is_flag=True, help="Enable verbose output.")
    @click.pass_context
    def cli_fn(ctx: click.Context, verbose: bool) -> None:
        """Royal FLush CLI"""
        ctx.ensure_object(dict)
        ctx.obj["VERBOSE"] = verbose

    # Add subcommands to the main group
    cli_fn.add_command(run_cmd)
    cli_fn.add_command(analyze_logs_cmd)
    cli_fn.add_command(version_cmd)
    cli_fn.add_command(create_template_cmd)

    return cli_fn


# Create a single instance of the CLI
cli = create_cli()

if __name__ == "__main__":
    sys.exit(cli.main())
