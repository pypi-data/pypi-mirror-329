import unittest
from pathlib import Path

from aioxmpp import JID

from royalflush.datatypes import GraphManager


class TestGraph(unittest.TestCase):

    def setUp(self) -> None:
        """
        Runs before each test. Ensures that the folder exists initially.
        """
        self.folder: Path = Path("royalflush_test_graphs")
        self.folder.mkdir(parents=True, exist_ok=True)

    def test_custom_graph(self) -> None:
        gml_manager = GraphManager()

        agent1 = JID.fromstr("agent1@localhost")
        agent2 = JID.fromstr("agent2@localhost")
        agent3 = JID.fromstr("agent3@localhost")
        agent4 = JID.fromstr("agent4@localhost")
        agent5 = JID.fromstr("agent5@localhost")
        agent6 = JID.fromstr("agent6@localhost")

        # Adding agents and connections
        gml_manager.add_agent(agent1, coalition_id=1)
        gml_manager.add_agent(agent2, coalition_id=1)
        gml_manager.add_agent(agent3, coalition_id=2)
        gml_manager.add_agent(agent4, coalition_id=2)
        gml_manager.add_agent(agent5, coalition_id=3)
        gml_manager.add_agent(agent6, coalition_id=None)

        gml_manager.add_connection(agent1, agent2)
        gml_manager.add_connection(agent2, agent3)
        gml_manager.add_connection(agent3, agent4)
        gml_manager.add_connection(agent4, agent2)
        gml_manager.add_connection(agent5, agent4)
        gml_manager.add_connection(agent6, agent4)

        # Exporting to GML
        out = self.folder / "agents_graph"
        gml_manager.export_to_gml(f"{out}.gml")
        gml_manager.import_from_gml(f"{out}.gml")

        # Visualizing the graph
        gml_manager.visualize(f"{out}.html")

    def test_tiny_complete_graph(self) -> None:
        num_agents = 3
        gml_manager = GraphManager()

        # Complete graph
        agents = [JID.fromstr(f"a{i}@localhost") for i in range(num_agents)]
        out = self.folder / f"{num_agents:03}_agents_complete"
        out.resolve()
        gml_manager.generate_complete(agents)
        gml_manager.export_to_gml(f"{out}.gml")
        gml_manager.import_from_gml(f"{out}.gml")
        gml_manager.visualize(f"{out}.html")

    def test_generated_graphs(self) -> None:
        gml_manager = GraphManager()
        for num_agents in [10, 50, 100]:
            agents = [JID.fromstr(f"a{i}@localhost") for i in range(num_agents)]

            # Generate a ring structure
            out = self.folder / f"{num_agents:03}_agents_ring"
            out.resolve()
            gml_manager.generate_ring(agents)
            gml_manager.export_to_gml(f"{out}.gml")
            gml_manager.import_from_gml(f"{out}.gml")
            gml_manager.visualize(f"{out}.html")

            # Complete graph
            out = self.folder / f"{num_agents:03}_agents_complete"
            out.resolve()
            gml_manager.generate_complete(agents)
            gml_manager.export_to_gml(f"{out}.gml")
            gml_manager.import_from_gml(f"{out}.gml")
            gml_manager.visualize(f"{out}.html")

            # Small-world graph
            out = self.folder / f"{num_agents:03}_agents_sw"
            out.resolve()
            gml_manager.generate_small_world(agents, k=4, p=0.3)
            gml_manager.export_to_gml(f"{out}.gml")
            gml_manager.import_from_gml(f"{out}.gml")
            gml_manager.visualize(f"{out}.html")
