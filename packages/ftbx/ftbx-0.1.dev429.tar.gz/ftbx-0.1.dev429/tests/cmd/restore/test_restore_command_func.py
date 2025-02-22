"""

    PROJECT: flex_toolbox
    FILENAME: test_restore_command_func.py
    AUTHOR: David NAISSE
    DATE: August 26th, 2024

    DESCRIPTION: restore_command_func function testing
"""

import argparse
import os
import shutil
from unittest import TestCase
from typer.testing import CliRunner
from ftbx import ftbx

runner = CliRunner()


class TestRestoreCommandFunc(TestCase):

    def test_restore_command_func_action(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script-restore",
                "--from",
                "cs-sbx",
            ],
        )

        push = runner.invoke(
            ftbx,
            [
                "push",
                "actions",
                "ftbx-script-restore",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
            ],
        )

        backup_name = os.listdir(
            os.path.join("cs-sbx", "actions", "ftbx-script-restore", "backup")
        )[0]

        restore = runner.invoke(
            ftbx,
            [
                "restore",
                "actions",
                "ftbx-script-restore",
                backup_name,
                "--in",
                "cs-sbx",
            ],
        )

        # tests
        assert (
            pull.exit_code == 0
            and push.exit_code == 0
            and restore.exit_code == 0
            and len(os.listdir("cs-sbx/actions/ftbx-script-restore/backup")) == 2
        )

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_restore_command_func_asset(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "assets",
                "--filters",
                "id=911",
                "--from",
                "cs-sbx",
            ],
        )

        push = runner.invoke(
            ftbx,
            [
                "push",
                "assets",
                "911",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
            ],
        )

        backup_name = os.listdir(
            os.path.join("cs-sbx", "assets", "911", "backup")
        )[0]

        restore = runner.invoke(
            ftbx,
            [
                "restore",
                "assets",
                "911",
                backup_name,
                "--in",
                "cs-sbx",
            ],
        )

        # tests
        assert (
            pull.exit_code == 0
            and push.exit_code == 0
            and restore.exit_code == 0
            and len(os.listdir("cs-sbx/assets/911/backup")) == 2
        )

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)

    def test_restore_command_func_backup_invalid(self):
        # ins
        pull = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script-restore",
                "--from",
                "cs-sbx",
            ],
        )

        push = runner.invoke(
            ftbx,
            [
                "push",
                "actions",
                "ftbx-script-restore",
                "--from",
                "cs-sbx",
                "--to",
                "cs-sbx",
            ],
        )

        backup_name = "doesnotexist" 

        restore = runner.invoke(
            ftbx,
            [
                "restore",
                "actions",
                "ftbx-script-restore",
                backup_name,
                "--in",
                "cs-sbx",
            ],
        )

        # tests
        assert (
            pull.exit_code == 0
            and push.exit_code == 0
            and restore.exit_code == 1
        )

        # reset
        shutil.rmtree("cs-sbx", ignore_errors=False, onerror=None)
