"""

    PROJECT: flex_toolbox
    FILENAME: test_retry_command_func.py
    AUTHOR: David NAISSE
    DATE: January 02, 2024

    DESCRIPTION: retry_command_func function testing
    
"""

import argparse
import json
import os.path
from unittest import TestCase
from typer.testing import CliRunner
from ftbx import ftbx

import pandas as pd

runner = CliRunner()


class TestRetryCommandFunc(TestCase):

    def test_retry_command_func_jobs(self):
        # ins
        result = runner.invoke(
            ftbx, ["retry", "jobs", "--filters", "limit=1", "--in", "cs-sbx"]
        )

        # test
        assert result.exit_code == 0

    def test_retry_command_func_workflows(self):
        # ins
        result = runner.invoke(
            ftbx, ["retry", "workflows", "--filters", "limit=1", "--in", "cs-sbx"]
        )

        # test
        assert result.exit_code == 0

    def test_retry_command_func_jobs_csv(self):
        # ins
        filename = "instances_to_be_retried.csv"
        df = pd.DataFrame([{"id": 724}])
        df.to_csv(filename)

        result = runner.invoke(
            ftbx, ["retry", "jobs", "--file", filename, "--in", "cs-sbx"]
        )

        # test
        assert result.exit_code == 0

        # reset
        os.remove(filename)

    def test_retry_command_func_jobs_json(self):
        # ins
        filename = "instances_to_be_retried.json"
        with open(filename, "a+") as instances_to_be_retried:
            json.dump(
                {"failed_jobs_1": {"id": 724}},
                instances_to_be_retried,
            )

        result = runner.invoke(
            ftbx, ["retry", "jobs", "--file", filename, "--in", "cs-sbx"]
        )

        # test
        assert result.exit_code == 0

        # reset
        os.remove(filename)

    def test_retry_command_func_invalid_json(self):
        # ins
        filename = "instances_to_be_retried.json"
        result = runner.invoke(
            ftbx, ["retry", "jobs", "--file", filename, "--in", "cs-sbx"]
        )

        assert result.exit_code == 1

    def test_retry_command_func_invalid_csv(self):
        # ins
        filename = "instances_to_be_retried.csv"
        result = runner.invoke(
            ftbx, ["retry", "jobs", "--file", filename, "--in", "cs-sbx"]
        )

        assert result.exit_code == 1
