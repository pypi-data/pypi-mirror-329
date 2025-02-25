"""Command to run the RoyalFlush experiment."""

import asyncio
import json
import logging
import sys
import traceback
import uuid
from pathlib import Path
from typing import Any, Dict

import click
import spade
from aioxmpp import JID

from royalflush import __version__

from .._agent.agent_factory import AgentFactory
from .._agent.coordinator import CoordinatorAgent
from .._agent.launcher import LauncherAgent
from .._agent.observer import ObserverAgent
from ..datatypes.experiment import ExperimentRawData
from ..datatypes.graph import GraphManager
from ..log.general import GeneralLogManager
from ..log.log import setup_loggers


async def main(experiment: ExperimentRawData) -> None:

    xmpp_domain = experiment.xmpp_domain
    max_message_size = 250_000  # shall not be close to 262 144
    number_of_observers = 1

    # UUID4
    uuid4: uuid.UUID | None = None
    if experiment.uuid4 == "generate_new_uuid4":
        uuid4 = uuid.uuid4()
    elif isinstance(experiment.uuid4, str):
        uuid4 = uuid.UUID(experiment.uuid4)

    # JIDs
    launcher_jid_str = f"launcher__{uuid4}@{xmpp_domain}"
    coordinator_jid_str = f"coordinator__{uuid4}@{xmpp_domain}"

    # Logging
    logger = GeneralLogManager(extra_logger_name="main")
    logger.info("Starting...")
    logger.info(f"Royal FLush version: {__version__}")
    logger.info(f"Python version: {sys.version}")
    logger.info(f"SPADE version: {spade.__version__}")
    logger.info(f"UUID4: {uuid4}")
    logger.info(f"Experiment details: {repr(experiment)}")

    # Graph
    logger.debug("Initializating GraphManager...")
    graph_manager = GraphManager()
    graph_manager.import_from_gml(experiment.graph_path)
    logger.debug(f"Graph {experiment.graph_path} loaded")

    # Coordinator
    logger.debug(f"Initializating {coordinator_jid_str} coordinator...")
    coordinator = CoordinatorAgent(
        jid=coordinator_jid_str,
        password="123",
        max_message_size=max_message_size,
        coordinated_agents=graph_manager.list_agents_jids(uuid=uuid4),
        verify_security=False,
    )
    await asyncio.sleep(0.2)

    # Observers
    # Observers will come in a future update.
    logger.debug("Initializating observers...")
    observer_jids: list[JID] = []
    for i in range(number_of_observers):
        observer_jids.append(JID.fromstr(f"o{i}__{uuid4}@{xmpp_domain}"))

    observers: list[ObserverAgent] = []
    for obs_jid in observer_jids:
        obs = ObserverAgent(
            jid=str(obs_jid),
            password="123",
            max_message_size=max_message_size,
            verify_security=False,
        )
        observers.append(obs)

    # Agent Factory
    logger.debug("Initializating agents...")
    agent_factory = AgentFactory(
        experiment=experiment,
        graph_manager=graph_manager,
        coordinator_jid=JID.fromstr(coordinator_jid_str),
        observer_jids=observer_jids,
        uuid=uuid4,
        max_message_size=max_message_size,
    )

    # Launcher
    logger.debug(f"Initializating {launcher_jid_str} launcher...")
    launcher = LauncherAgent(
        jid=launcher_jid_str,
        password="123",
        max_message_size=max_message_size,
        agents=agent_factory.create_agents(),
        agents_coordinator=coordinator.jid,
        agents_observers=observer_jids,
        verify_security=False,
    )

    try:
        logger.info("Starting observers...")
        for observer in observers:
            await observer.start()
        await asyncio.sleep(0.2)
        logger.info("Observers initialized.")

        logger.info("Starting coordinator...")
        await coordinator.start()
        await asyncio.sleep(0.2)
        logger.info("Coordinator initialized.")

        logger.info("Starting launcher...")
        await launcher.start()
        await asyncio.sleep(0.2)
        logger.info("Launcher initialized.")

        await asyncio.sleep(5)
        while not coordinator.ready_to_start_algorithm or any(ag.is_alive() for ag in launcher.agents):
            await asyncio.sleep(5)

    except KeyboardInterrupt as e:
        raise e

    except Exception as e:
        logger.exception(e)
        traceback.print_exc()

    finally:
        logger.info("Stopping...")
        if coordinator.is_alive():
            await coordinator.stop()
        if launcher.is_alive():
            await launcher.stop()
        for ag in launcher.agents:
            if ag.is_alive():
                await ag.stop()
        logger.info("Run finished.")


def init_experiment(experiment: ExperimentRawData) -> None:
    try:
        setup_loggers(general_level=logging.INFO)
        spade.run(main(experiment=experiment))
    except KeyboardInterrupt:
        pass
    except Exception:
        traceback.print_exc()


@click.command(name="run")
@click.argument("experiment_file", type=click.Path())
@click.pass_context
def run_cmd(ctx: click.Context, experiment_file: str) -> None:
    """
    Run the main RoyalFlush application with the provided JSON experiment file.

    Usage:
        royalflush run experiment.json

    Args:
        ctx (click.Context): The Click context object.
        experiment_file (str): Path to the JSON experiment file to load.
    """
    file_path: Path = Path(experiment_file)
    if not file_path.is_file():
        click.echo(f"Error: File '{experiment_file}' does not exist or it is not a file.")
        return

    if file_path.suffix.lower() != ".json":
        click.echo("Error: Only .json experiment files are supported.")
        return

    # Load JSON
    try:
        config_data: Dict[str, Any] = json.loads(file_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        click.echo(f"Error loading JSON data: {exc}")
        return

    experiment = ExperimentRawData.from_json(config_data)

    if ctx.obj.get("VERBOSE"):
        click.echo(f"Experiment loaded: {experiment}")

    init_experiment(experiment=experiment)
