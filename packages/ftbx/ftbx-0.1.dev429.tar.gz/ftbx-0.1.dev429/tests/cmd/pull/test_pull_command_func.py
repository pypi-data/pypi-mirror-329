"""

    PROJECT: flex_toolbox
    FILENAME: test_pull_command_func.py
    AUTHOR: David NAISSE
    DATE: January 04, 2024

    DESCRIPTION: pull_command_func function testing
    
"""

import os
import shutil
from unittest import TestCase
from typer.testing import CliRunner
from ftbx import ftbx
from src._environment import Environment


runner = CliRunner()


class TestPullCommandFunc(TestCase):

    def test_pull_command_func_account_property(self):
        # ins
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "accountProperties",
                "--post-filters",
                "key=ftbx-account-property",
                "--from",
                "cs-sbx"
            ]
        )

        assert result.exit_code == 0 and "1/1" in result.stdout and os.path.isdir("cs-sbx/accountProperties")

    def test_pull_command_func_invalid_env(self):
        # ins
        result = runner.invoke(
            ftbx, ["pull", "actions", "--filters", "limit=1", "--from", "doesnotexist"]
        )

        assert result.exit_code == 1

    def test_pull_command_func_object_name(self):
        # ins
        result = runner.invoke(
            ftbx, ["pull", "actions", "ftbx-script" ,"--from", "cs-sbx"]
        )

        assert result.exit_code == 0 and "1/1" in result.stdout and os.path.isdir("cs-sbx/actions/ftbx-script")

    def test_pull_command_func_object_id(self):
        # ins
        result = runner.invoke(
            ftbx, ["pull", "workflowDefinitions", "550" ,"--from", "cs-sbx"]
        )

        assert result.exit_code == 0 and "1/1" in result.stdout and os.path.isdir("cs-sbx/workflowDefinitions")

    def test_pull_command_func_no_filters(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--from",
                environment.name,
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
            and os.path.isfile(
                os.path.join(
                    environment.name, "actions", "ftbx-script", "script.groovy"
                )
            )
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_jef_script_with_imports(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script",
                "--filters",
                "limit=1",
                "--from",
                environment.name,
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and "1/1" in result.stdout
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
            and os.path.isfile(
                os.path.join(
                    environment.name, "actions", "ftbx-script", "script.groovy"
                )
            )
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_envs(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script",
                "--filters",
                "limit=1",
                "--from",
                "cs-sbx",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_filters_classic(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script",
                "--filters",
                "limit=1",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_filters_fql(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "fql=(name~ftbx)",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_with_dependencies(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "workflowDefinitions",
                "--filters",
                "name=ftbx-workflow-pull-with-dependencies",
                "--from",
                "cs-sbx",
                "--with-dependencies",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(
                os.path.join(environment.name, "actions", "ftbx-create-placeholder")
            )
            and os.path.isdir(
                os.path.join(environment.name, "actions", "ftbx-create-proxy")
            )
            and os.path.isdir(
                os.path.join(
                    environment.name, "actions", "ftbx-extract-technical-metadata"
                )
            )
            and os.path.isdir(
                os.path.join(environment.name, "actions", "ftbx-import-asset")
            )
            and os.path.isdir(
                os.path.join(environment.name, "actions", "ftbx-multi-decision")
            )
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
            and os.path.isdir(
                os.path.join(environment.name, "resources", "ftbx-resource")
            )
            and os.path.isdir(
                os.path.join(
                    environment.name, "taskDefinitions", "ftbx-task-dependency"
                )
            )
            and os.path.isdir(
                os.path.join(environment.name, "wizards", "ftbx-wizard-task-dependency")
            )
            and os.path.isdir(
                os.path.join(
                    environment.name,
                    "workflowDefinitions",
                    "ftbx-workflow-pull-with-dependencies",
                )
            )
            and os.path.isfile(
                os.path.join(
                    environment.name,
                    "workflowDefinitions",
                    "ftbx-workflow-pull-with-dependencies",
                    "graph.png",
                )
            )
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_int(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script",
                "--post-filters",
                "concurrentJobsLimit=0",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_list(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "jobs",
                "--filters",
                "status=Completed",
                "--filters",
                "limit=1",
                "--post-filters",
                "history.events[0].message~system completed",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "jobs"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_bool(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script",
                "--post-filters",
                "enabled=True",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_string(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script",
                "--post-filters",
                "name=ftbx-script",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_several_post_filters_text(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            [
                "pull",
                "actions",
                "--filters",
                "name=ftbx-script",
                "--post-filters",
                "configuration.instance[text]~execute()",
                "--from",
                "cs-sbx",
            ],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)

    def test_pull_command_func_all(self):
        # ins
        environment = Environment.from_env_file(environment="cs-sbx")
        result = runner.invoke(
            ftbx,
            ["pull", "all", "--from", "cs-sbx"],
        )

        # test
        assert (
            result.exit_code == 0
            and os.path.isdir(environment.name)
            and os.path.isdir(os.path.join(environment.name, "actions", "ftbx-script"))
            and os.path.isdir(os.path.join(environment.name, "taxonomies"))
            and os.path.isdir(os.path.join(environment.name, "workspaces"))
        )

        # reset
        shutil.rmtree(environment.name, ignore_errors=False, onerror=None)
