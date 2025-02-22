"""

    PROJECT: flex_toolbox
    FILENAME: test_connect_command_func.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: connect_command_func function testing
    
"""

import requests
from unittest import TestCase
from src._encryption import decrypt_pwd
from src._environment import Environment
from typer.testing import CliRunner
from ftbx import ftbx

runner = CliRunner()


class TestConnectCommandFunc(TestCase):

    def test_connect_command_func_known_full_alias(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "connect",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and Environment.get_default_environment_alias() == "cs-sbx"
        )

    def test_connect_command_func_wrong_alias(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "connect",
                "this-alias-does-not-exist",
            ],
        )

        # tests
        assert result.exit_code == 1

    def test_connect_command_func_update(self):
        # ins
        env = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "connect",
                env.url,
                env.username,
                decrypt_pwd(env.password),
                "--alias",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and Environment.from_env_file(environment="cs-sbx").username == env.username
        )

    def test_connect_command_func_new_invalid_url(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "connect",
                "https://bad_url",
                "bad_username",
                "bad_password",
                "--alias",
                "bad_alias",
            ],
        )

        # tests
        assert result.exit_code == 1

    def test_connect_command_func_new_invalid_password(self):
        # ins
        env = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "connect",
                env.url,
                env.username,
                "bad_password",
                "--alias",
                "cs-sbx",
            ],
        )

        # tests
        assert result.exit_code == 1
