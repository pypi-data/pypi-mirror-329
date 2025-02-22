"""

    PROJECT: flex_toolbox
    FILENAME: test_query_command_func.py
    AUTHOR: David NAISSE
    DATE: January 03, 2024

    DESCRIPTION: query_command_func function testing
"""

import json
import os.path
from unittest import TestCase
from typer.testing import CliRunner
from ftbx import ftbx

runner = CliRunner()


class TestQueryCommandFunc(TestCase):

    def test_query_command_func_alias(self):
        # ins
        result = runner.invoke(
            ftbx, ["query", "GET", "resources;limit=1", "--from", "cs-sbx"]
        )

        # test
        assert result.exit_code == 0 and os.path.isfile("query.json")

        # reset
        os.remove("query.json")

    def test_query_command_func_payload_cli(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "query",
                "POST",
                "jobs/819/actions",
                "--payload",
                "action=retry",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert result.exit_code == 0 and os.path.isfile("query.json")

        # reset
        os.remove("query.json")

    def test_query_command_func_payload_file(self):
        # ins
        with open("query_config.json", "w") as query_config_file:
            json.dump({"action": "retry"}, query_config_file)

        result = runner.invoke(
            ftbx,
            [
                "query",
                "POST",
                "jobs/724/actions",
                "--payload",
                "query_config.json",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isfile("query_config.json")
            and os.path.isfile("query.json")
        )

        # reset
        os.remove("query.json")
        os.remove("query_config.json")
