"""

    PROJECT: flex_toolbox
    FILENAME: test_list_command_func.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: list_command_func function testing
    
"""

import os
import shutil
from unittest import TestCase
from typer.testing import CliRunner
from ftbx import ftbx

runner = CliRunner()


class TestListCommandFunc(TestCase):

    def test_list_command_func_account_properties(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "accountProperties",
                "--post-filters",
                "key=ftbx-account-property",
            ],
        )

        assert result.exit_code == 0

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_valid_all(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "assets",
                "--from",
                "cs-sbx",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_filters_classic(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "assets",
                "--from",
                "cs-sbx",
                "--filters",
                "limit=1",
                "--filters",
                "name=ftbx-placeholder",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_filters_fql(self):
        # ins
        result = runner.invoke(
            ftbx, ["list", "assets", "--from", "cs-sbx", "--filters", "fql=(name~ftbx)"]
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_int(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "actions",
                "--from",
                "cs-sbx",
                "--post-filters",
                "concurrentJobsLimit=0",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_bool(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "actions",
                "--from",
                "cs-sbx",
                "--post-filters",
                "enabled=true",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_string(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "actions",
                "--from",
                "cs-sbx",
                "--post-filters",
                "name~ftbx",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_list(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "workflows",
                "--from",
                "cs-sbx",
                "--filters",
                "status=Completed",
                "--filters",
                "limit=1",
                "--post-filters",
                "jobs.jobs[-1].status=Completed",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_post_filters_text(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "jobs",
                "--from",
                "cs-sbx",
                "--filters",
                "status=Completed",
                "--filters",
                "limit=1",
                "--post-filters",
                "history[text]~completed",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_taxonomies(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "taxonomies",
                "--from",
                "cs-sbx",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_tags_collections(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "list",
                "taxonomies",
                "--from",
                "cs-sbx",
            ],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)

    def test_list_command_func_adaptive_sub_items(self):
        # ins
        result = runner.invoke(
            ftbx,
            ["list", "workflows", "--from", "cs-sbx", "--filters", "limit=1"],
        )

        # tests
        assert result.exit_code == 0 and os.path.isdir("lists")

        # reset
        shutil.rmtree("lists", ignore_errors=False, onerror=None)
