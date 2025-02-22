"""

    PROJECT: flex_toolbox
    FILENAME: test_env.py
    AUTHOR: David NAISSE
    DATE: August 13th, 2024

    DESCRIPTION: env function testing
    
"""

from unittest import TestCase
from typer.testing import CliRunner
from ftbx import ftbx

runner = CliRunner()


class TestEnv(TestCase):

    def test_env_valid(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "env"
            ]
        )

        # tests
        assert result.exit_code == 0
