import json
import os
import unittest

from click.testing import CliRunner

from royalflush.cli import cli
from royalflush.datatypes import ExperimentRawData


class TestCli(unittest.TestCase):
    """Test suite for RoyalFlush CLI commands."""

    def setUp(self) -> None:
        """
        Runs before each test. Ensures test file does not exist initially.
        """
        self.test_filename = "test_cli_experiment.json"
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def tearDown(self) -> None:
        """
        Runs after each test. Cleans up the test file if it still exists.
        """
        if os.path.exists(self.test_filename):
            os.remove(self.test_filename)

    def test_create_template_cmd(self) -> None:
        """
        Test creating a template JSON file, loading it into the Experiment class,
        and verifying the fields are correct.
        """
        # Invoke the 'create-template' command with CliRunner
        runner = CliRunner()
        result = runner.invoke(cli, ["create-template", self.test_filename])
        self.assertEqual(result.exit_code, 0, msg=f"CLI error output: {result.output}")

        # Verify the file is created
        self.assertTrue(os.path.exists(self.test_filename))

        # Load the JSON into the Experiment class
        with open(self.test_filename, "r", encoding="utf-8") as f:
            data = json.load(f)
        experiment = ExperimentRawData.from_json(data)

        # Check if the data was imported correctly
        # algorithm is stored in lowercase in Experiment.__init__()
        self.assertEqual(experiment.uuid4, "generate_new_uuid4")
        self.assertEqual(experiment.algorithm, "acol")
        self.assertEqual(experiment.algorithm_rounds, 10)
        self.assertEqual(experiment.consensus_iterations, 10)
        self.assertEqual(experiment.training_epochs, 1)
        self.assertEqual(experiment.graph_path, "/data/user/graphs/star.gml")
        self.assertEqual(experiment.dataset, "cifar100")
        self.assertEqual(experiment.distribution, "non_iid diritchlet 0.1")
        self.assertEqual(experiment.ann, "cnn5")

        # Delete the file and confirm
        os.remove(self.test_filename)
        self.assertFalse(os.path.exists(self.test_filename))


if __name__ == "__main__":
    unittest.main()
