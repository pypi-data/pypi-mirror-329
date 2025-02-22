"""

    PROJECT: flex_toolbox
    FILENAME: test_compare_command_func.py
    AUTHOR: David NAISSE
    DATE: January 05, 2024

    DESCRIPTION: compare_command_func function testing
    
"""

import os.path
import shutil
from unittest import TestCase
from typer.testing import CliRunner
from ftbx import ftbx

runner = CliRunner()


class TestCompareCommandFunc(TestCase):

    def test_compare_command_func_valid(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "compare",
                "actions",
                "cs-sbx",
                "cs-sbx",
                "--filters",
                "name=ftbx-script",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir("compare_cs-sbx_cs-sbx")
            and os.path.isdir(os.path.join("compare_cs-sbx_cs-sbx", "actions"))
        )

        # reset
        shutil.rmtree("compare_cs-sbx_cs-sbx", ignore_errors=False, onerror=None)

    def test_compare_command_func_missing_env(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "compare",
                "actions",
                "cs-sbx",
                "--filters",
                "name=ftbx-script",
            ],
        )

        # test
        assert result.exit_code == 1

    def test_compare_command_func_env_not_exist(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "compare",
                "actions",
                "not-exist",
                "not-exist-either",
                "--filters",
                "name=ftbx-script",
            ],
        )

        # tests
        assert result.exit_code == 1
