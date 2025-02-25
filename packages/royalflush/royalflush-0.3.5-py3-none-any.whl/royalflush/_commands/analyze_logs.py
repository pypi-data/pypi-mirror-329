"""Command to analyze logs from a previous run."""

from pathlib import Path
from typing import List

import click
import pandas as pd
import plotly.express as px


def load_dataset(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def extract_agent_name(data: pd.DataFrame) -> pd.DataFrame:
    data["agent_name"] = data["agent"].str.split("@").str[0]
    return data


def get_unique_layers(data: pd.DataFrame) -> List[str]:
    return data["layer"].unique().tolist()


def generate_line_plots(data: pd.DataFrame, unique_layers: List[str]) -> None:
    for layer in unique_layers:
        # Filter data for the current layer
        layer_data = data[data["layer"] == layer]

        # Create the line plot
        fig = px.line(
            layer_data,
            x="algorithm_round",
            y="weight",
            color="agent_name",
            title=f"Convergence of Weights for Layer: {layer}",
            labels={"algorithm_round": "Epoch", "weight": "Weight Value", "agent_name": "Agent"},
        )

        # Update layout for better aesthetics
        fig.update_layout(legend_title="Agents", title_x=0.5)

        # Show the plot
        fig.show()


@click.command(name="analyze-logs")
@click.argument("experiment_folder", type=click.Path())
@click.pass_context
def analyze_logs_cmd(ctx: click.Context, experiment_folder: str) -> None:
    """
    Analyze logs from a previous run inside the given folder.

    Usage:
        royalflush analyze-logs experiment_folder

    Args:
        ctx (click.Context): The Click context object.
        experiment_folder (str): Path to the folder containing logs from a previous run.
    """
    folder_path: Path = Path(experiment_folder)
    if not folder_path.is_dir():
        click.echo(f"Error: '{experiment_folder}' is not a valid directory.")
        return

    if ctx.obj.get("VERBOSE"):
        click.echo(f"Analyzing logs in folder: {experiment_folder}")

    # Test with convergence of weights
    file_path: str = f"{experiment_folder}/nn_convergence.csv"
    data: pd.DataFrame = load_dataset(file_path)
    data = extract_agent_name(data)
    unique_layers: List[str] = get_unique_layers(data)
    generate_line_plots(data, unique_layers)

    click.echo("Log analysis complete.")
