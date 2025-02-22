"""

    PROJECT: flex_toolbox
    FILENAME: test_launch_command_func.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: launch_command_func funciton testing
    
"""

import json
import os
from unittest import TestCase
from typer.testing import CliRunner
from ftbx import ftbx

runner = CliRunner()


class TestLaunchCommandFunc(TestCase):

    def test_launch_command_func_all_valid(self):
        # ins
        result = runner.invoke(
            ftbx, ["launch", "jobs", "ftbx-script-completes", "--in", "cs-sbx"]
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("cs-sbx/jobs/")

    def test_launch_command_func_env_name_invalid(self):
        # ins
        result = runner.invoke(
            ftbx, ["launch", "jobs", "ftbx-scrip-completes", "--in", "does-not-exist"]
        )

        # tests
        assert result.exit_code == 1

    def test_launch_command_func_object_name_invalid(self):
        # ins
        result = runner.invoke(
            ftbx, ["launch", "jobs", "does-not-exist", "--in", "cs-sbx"]
        )

        # tests
        assert result.exit_code == 1

    def test_launch_command_func_params_valid(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "launch",
                "jobs",
                "ftbx-script-completes",
                "--in",
                "cs-sbx",
                "--params",
                "assetId=511",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("cs-sbx/jobs/")

    def test_launch_command_func_params_invalid(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "launch",
                "jobs",
                "ftbx-script-completes",
                "--in",
                "cs-sbx",
                "--params",
                "assetId=111",
                "--params",
                "workspaceId=405",
            ],
        )

        # tests
        assert result.exit_code == 1

    def test_launch_command_func_params_file(self):
        # ins
        with open("launch_params.json", "w") as launch_params_file:
            json.dump({"assetId": 511}, launch_params_file)

        result = runner.invoke(
            ftbx,
            [
                "launch",
                "jobs",
                "ftbx-script-completes",
                "--in",
                "cs-sbx",
                "--from-file",
                "launch_params.json",
            ],
        )

        # tests
        assert (
            result.exit_code == 0
            and os.path.isfile("launch_params.json")
            and os.path.isdir("cs-sbx/jobs")
        )

        # reset
        os.remove("launch_params.json")
