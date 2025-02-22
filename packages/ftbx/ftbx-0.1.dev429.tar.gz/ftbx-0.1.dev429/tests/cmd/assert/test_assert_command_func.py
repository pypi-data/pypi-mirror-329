"""

    PROJECT: flex_toolbox
    FILENAME: test_assert_command_func.py
    AUTHOR: David NAISSE
    DATE: August 28th, 2024

    DESCRIPTION: assert_command_func function testing
    
"""

from typer.testing import CliRunner
from unittest import TestCase
from ftbx import ftbx

runner = CliRunner()


class TestAssertCommandFunc(TestCase):

    def test_assert_command_func_true_with_id(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "assert",
                "actions",
                "ftbx-script",
                "concurrentJobsLimit=0",
                "configuration.instance.execution-lock-type=NONE",
                "--in",
                "cs-sbx",
            ],
        )

        # tests
        assert result.exit_code == 0
        assert "True" in result.stdout

    def test_assert_command_func_false_with_name(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "assert",
                "assets",
                "911",
                "deleted=False",
                "name=wrong-name",
                "--in",
                "cs-sbx",
            ],
        )

        # tests
        assert result.exit_code == 0
        assert "False" in result.stdout
