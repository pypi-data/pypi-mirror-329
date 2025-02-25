"""Command to create a JSON template for the RoyalFlush experiment."""

import json
from pathlib import Path

import click


@click.command(name="create-template")
@click.argument("template_file", required=False)
@click.pass_context
def create_template_cmd(_: click.Context, template_file: str) -> None:
    """
    Create a JSON template for the experiment.

    Usage:
      royalflush create-template [<filename>]

    If <filename> is not provided, it defaults to 'template.json'.

    Example:
      royalflush create-template
      royalflush create-template experiment.json

    The resulting JSON has the following structure:
    {
        "uuid4": "generate_new_uuid4",
        "xmpp_domain": "localhost",
        "algorithm": "ACoL",
        "algorithm_rounds": 10,
        "consensus_iterations": 10,
        "training_epochs": 1,
        "graph_path": "/data/user/graphs/star.gml",
        "dataset": "cifar100",
        "distribution": "non_iid diritchlet 0.1",
        "ann": "cnn5"
    }

    Args:
        ctx (click.Context): The Click context object.
        template_file (str): Filename where the JSON is created. Defaults to "template.json".
    """
    if not template_file:
        template_file = "template.json"

    file_path = Path(template_file)

    if file_path.exists():
        click.echo(f"Error: File '{template_file}' already exists.")
        return

    template_data = {
        "uuid4": "generate_new_uuid4",
        "xmpp_domain": "localhost",
        "algorithm": "ACoL",
        "algorithm_rounds": 10,
        "consensus_iterations": 10,
        "training_epochs": 1,
        "graph_path": "/data/user/graphs/star.gml",
        "dataset": "cifar100",
        "distribution": "non_iid diritchlet 0.1",
        "ann": "cnn5",
    }

    try:
        file_path.write_text(json.dumps(template_data, indent=4), encoding="utf-8")
    except OSError as exc:
        click.echo(f"Error creating template file: {exc}")
        return

    click.echo(f"Template created at '{template_file}'.")
